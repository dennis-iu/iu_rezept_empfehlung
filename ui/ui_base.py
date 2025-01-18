import importlib
import logging as log
import webbrowser
from abc import ABC
from io import BytesIO
from tkinter import (Button, Canvas, Checkbutton, Entry, IntVar, Label,
                     PhotoImage, Scale, StringVar, Toplevel, messagebox)

import requests
from PIL import Image, ImageTk

from src.recipe_api import RecipeApi


class UiBase(ABC):
    """Basis-Klasse für alle Dashboards."""

    def __init__(self, master, config):
        """
        Klasse initialisieren.

        :param master: tkinter objekt
        :param config: dict - Konfigurationsdaten
        :return: None
        """
        # Parameter als Klassen-Variablen initalisieren
        self.config = config
        self.window = master

        # Standard Fenster herstellen
        self.standard_window()

    def standard_window(self):
        """Methode um das Standard Fenster herzustellen."""
        self.window.geometry("600x400")
        self.window.configure(bg="#FFFFFF")

        # Linker Canvas
        self.left_canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=400,
            width=300,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.left_canvas.place(x=0, y=0)

        # Bild links einfügen
        self.image_image_logo = PhotoImage(
            file=self.config["assets_path"] + "image_logo.png"
        )
        self.image_logo = self.left_canvas.create_image(
            150.0, 200.0, image=self.image_image_logo
        )

        # Rechter Canvas (standard)
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=400,
            width=300,  # Halbe Breite des Fensters
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=300, y=0)

        self.canvas.create_rectangle(0.0, 0.0, 300.0, 400.0, fill="#91C4FF", outline="")

        log.info("Standard Fenster hergestellt!")

    def switch_to(self, new_dashboard_class):
        """
        Methode um zu einem anderen Dashboard zu wechseln.

        :param new_dashboard_class: class - Dashboards zu dem gewechselt werden soll
        :return: None
        """
        # Altes Dashboard zurücksetzen
        for widget in self.window.winfo_children():
            widget.destroy()

        # Neues Dashboard laden
        new_dashboard_class(self.window, self.config)

    def open_link(self, link):
        """
        Methode um einen Link im Chromium Browser zu öffnen.

        :param link: str - Link zur Seite die geöffnet werden soll
        :return: None
        """
        browser = webbrowser.get("chromium-browser")
        browser.open(link)

    def create_button(self, name, to_do, position, anchor="center"):
        """
        Methode um einen Button im Canvas zu integrieren.

        :param name: str - Name des Buttons (der Datei in Assets)
        :param to_do: function - Funktion die der Button ausführen soll
        :param position: dict - Position des Buttons (z. B. {"x": 50.0, "y": 50.0})
        :param anchor: str - Ausrichtung des Buttons (Default - center)
        :return: None
        """
        # Bilder laden
        button_image = PhotoImage(
            file=self.config["assets_path"] + "button_" + name + ".png"
        )

        button_image_hover = PhotoImage(
            file=self.config["assets_path"] + "button_hover_" + name + ".png"
        )

        # Button-Widget erstellen
        button = self.canvas.create_image(
            position["x"], position["y"], image=button_image, anchor=anchor
        )

        # Funktionen für Hover-Effekte
        def on_enter(event):
            """
            Funktion zum reagieren auf das hover event.

            :param event: event - enter event
            :return: None
            """
            self.canvas.itemconfig(button, image=button_image_hover)

        def on_leave(event):
            """
            Funktion zum reagieren auf das leave event.

            :param event: event - leave event
            :return: None
            """
            self.canvas.itemconfig(button, image=button_image)

        def on_click(event):
            """
            Funktion zum reagieren auf das click event.

            :param event: event - click event
            :return: None
            """
            to_do()

        # Event-Bindings
        self.canvas.tag_bind(button, "<Enter>", on_enter)
        self.canvas.tag_bind(button, "<Leave>", on_leave)
        self.canvas.tag_bind(button, "<Button-1>", on_click)

        # Speicher Bilder, damit sie nicht vom Garbage Collector gelöscht werden
        self.canvas.image_dict = getattr(self.canvas, "image_dict", {})
        self.canvas.image_dict[name] = (button_image, button_image_hover)

    def create_entry(self, position):
        """
        Methode um ein Eingabefenster im Canvas zu integrieren.

        :param position: dict - Position des Entrys (z. B. {"x": 50.0, "y": 50.0, "width": 50.0, "height": 50.0})
        :return: None
        """
        entry_image = PhotoImage(file=self.config["assets_path"] + "entry.png")
        entry_bg = self.canvas.create_image(450.5, 206.0, image=entry_image)
        self.entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry.place(**position)

    def create_multiselect_dropdown(
        self, name, options, position, width=265, height=28, bg_color="#FFFFFF"
    ):
        """
        Methode, um ein Dropdown-Menü mit Mehrfachauswahl im Canvas zu integrieren.

        :param name: str - Name des Dropdowns
        :param options: list - Liste der Auswahlmöglichkeiten
        :param position: dict - Position des Dropdowns (z. B. {"x": 50.0, "y": 50.0})
        :param width: int - Breite des Dropdowns (Default - 265)
        :param height: int - Höhe des Dropdowns (Default - 28)
        :param bg_color: str - Hintergrundfarbe des Dropdowns (Default - weiß)
        :return: None
        """
        # Variablen initialisieren
        if not hasattr(self, "dropdown_references"):
            self.dropdown_references = {}

        # Haupt-Label
        label_text = StringVar(value="Mehrfachauswahl")

        label = Label(
            self.canvas,
            textvariable=label_text,
            bg=bg_color,
            relief="flat",
            highlightbackground="#CCCCCC",
            highlightthickness=2,
        )
        label.place(x=position["x"], y=position["y"], width=width, height=height)

        # Speichere Optionen und Status
        selected_vars = [IntVar() for _ in options]
        self.dropdown_references[name] = {
            "label": label,
            "options": options,
            "selected_vars": selected_vars,
        }

        # Dropdown anzeigen
        def show_dropdown(event):
            """
            Methode um das Dropdown Menü basierend auf dem Event anzupassen.

            :param event: event - change event
            :return: None
            """
            if hasattr(self, f"{name}_dropdown_window"):
                getattr(self, f"{name}_dropdown_window").destroy()

            dropdown_window = Toplevel()
            dropdown_window.geometry(
                "+{}+{}".format(event.x_root, event.y_root + height)
            )
            dropdown_window.overrideredirect(True)

            # Checkboxen hinzufügen
            def update_label():
                """Label aktualisieren."""
                selected_values = [
                    option for option, var in zip(options, selected_vars) if var.get()
                ]
                label_text.set(
                    ", ".join(selected_values) if selected_values else "Mehrfachauswahl"
                )

            for i, option in enumerate(options):
                Checkbutton(
                    dropdown_window,
                    text=option,
                    variable=selected_vars[i],
                    onvalue=1,
                    offvalue=0,
                    bg=bg_color,
                    anchor="w",
                    command=update_label,
                ).pack(fill="x", padx=5, pady=2)

            # OK-Button zum Schließen
            def close_dropdown():
                """Dropdown schließen."""
                dropdown_window.destroy()

            Button(
                dropdown_window, text="Ok", command=close_dropdown, bg=bg_color
            ).pack(fill="x", padx=5, pady=5)

            setattr(self, f"{name}_dropdown_window", dropdown_window)

        # Label anklickbar machen
        label.bind("<Button-1>", show_dropdown)

    def create_calorie_slider(
        self,
        position,
        min_value=0,
        max_value=2000,
        step=10,
        width=265,
        height=28,
        bg_color="#FFFFFF",
    ):
        """
        Funktion, um einen Slider für die maximale Kalorienanzahl im Canvas zu integrieren.

        :param position: dict - Position des Sliders (z. B. {"x": 50.0, "y": 50.0})
        :param min_value: int - Minimaler Wert des Sliders (Default - 0)
        :param max_value: int - Maximaler Wert des Sliders (Default - 2000)
        :param step: int - Schrittweite des Sliders (Default - 10)
        :param width: int - Breite des Sliders (Default - 265)
        :param height: int - Höhe des Sliders (Default - 28)
        :param bg: str - Hintergrundfarbe des Sliders (Default - weiß)
        :return: None
        """
        # Variable zur Speicherung des maximal auswählbaren Wertes
        calorie_value = IntVar(value=max_value)

        # Hintergrund-Etikett für den Slider
        label_bg = Label(self.canvas, bg=bg_color, text="", width=width, height=height)
        label_bg.place(x=position["x"], y=position["y"], width=width, height=height)

        # Anzeige des aktuellen Werts (max-wert)
        value_display = Label(
            self.canvas,
            text=f"{max_value} kcal",
            bg=bg_color,
            fg="#000716",
            anchor="w",
            padx=5,
        )
        value_display.place(x=position["x"], y=position["y"] - 20, width=width)

        # Slider integrieren
        slider = Scale(
            self.canvas,
            from_=min_value,
            to=max_value,
            orient="horizontal",
            resolution=step,
            showvalue=0,
            variable=calorie_value,
            bg=bg_color,
            fg="#000716",
            highlightthickness=0,
            troughcolor="#CCCCCC",
            sliderrelief="flat",
        )
        slider.place(x=position["x"], y=position["y"], width=width, height=height)

        # Aktualisierung der Anzeige bei Änderung des Werts
        def update_value_display(value):
            """
            Methode um den angezeigten Wert anzupassen.

            :param value: string - Neuer Wert
            :return: None
            """
            value_display.config(text=f"{value} kcal")

        slider.config(command=update_value_display)

        # Refernzen speichern
        if not hasattr(self, "slider_references"):
            self.slider_references = {}
        self.slider_references["calorie_slider"] = {
            "slider": slider,
            "value_display": value_display,
            "calorie_value": calorie_value,
        }

    def create_dynamic_text(self, input, position, fontsize=15 * -1, anchor="center"):
        """
        Funktion, um einen Text im Standard auf dem Dashboard zu integrieren.

        :param input: str - Textinput
        :param position: dict - Position des Textes (z. B. {"x": 50.0, "y": 50.0})
        :param fontsize: int - Größe der Schrift (Default - 15 * -1)
        :param anchor: str - Ausrichtung des Textes (Default - center)
        :return: None
        """
        self.canvas.create_text(
            position["x"],
            position["y"],
            anchor=anchor,
            text=input,
            fill="#FFFFFF",
            font=("Inter ExtraBold", fontsize),
        )

    def create_dynamic_image(
        self, image_url, position, size=(150, 110), anchor="center"
    ):
        """
        Funktion, um ein Bild über seine URL auf dem Dashboard zu integrieren.

        :param image_url: str - Url des Bildes
        :param position: dict - Position des Textes (z. B. {"x": 50.0, "y": 50.0})
        :param size: tuple - Größe die das Bild haben soll (Default - 150,110)
        :param anchor: str - Ausrichtung des Bildes (Default - center)
        :return: None
        """
        # Bild herunterladen
        response = requests.get(image_url)
        response.raise_for_status()

        # Bild mit Pillow Package öffnen
        image_data = BytesIO(response.content)
        pil_image = Image.open(image_data)

        # Größe des Bildes anpassen
        pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)

        # Konvertierung in Tkinter Image
        self.tk_image = ImageTk.PhotoImage(pil_image)

        # Bild in den Canvas integrieren
        self.canvas.create_image(
            position["x"], position["y"], image=self.tk_image, anchor=anchor
        )

    def make_request(self, input=None, retry=False):
        """
        Funktion, um den Api-Request basierend auf den Eingaben auszuführen.

        :param input: dict - Eingabedaten (Default - None)
        :param retry: bool - Erneut oder neue Eingabe? (Default - False)
        :return: resultset
        """
        relevant_inputs = ["query", "intolerances", "maxCalories"]
        if retry == True:
            self.config["payload"]["offset"] += 1
        else:
            for key in relevant_inputs:
                self.config["payload"].pop(key, None)
            self.config["payload"].update(input)
            self.config["payload"]["offset"] = 0

        if self.config.get("recipe", None) is not None:
            self.config["recipe"] = {}
        try:
            with RecipeApi(self.config) as ra:
                recipe = ra.send_request()
                log.info("Request gesendet.")
                self.config.update({"recipe": recipe})
        except Exception as e:
            log.error(f"Exception: {e}")
            self.show_error_dialog("Konnte Request nicht ausführen.")
            search_module = importlib.import_module(
                "ui.search"
            )  # Um Circular Import Probleme zu verhindern
            SearchUi = search_module.SearchUi
            self.switch_to(SearchUi)

    def show_error_dialog(self, message):
        """
        Methode um die Error-Nachricht anzuzeigen

        :param path: str - Error-Nachricht
        :return: None
        """
        messagebox.showerror("Fehler", message)
