import re

from deep_translator import GoogleTranslator

from ui.result import ResultUi
from ui.ui_base import UiBase


class SearchUi(UiBase):
    """Klasse für das Search-Dashboard."""

    def __init__(self, master, config):
        """
        Initialisieren der Klasse.

        :param master: tkinter objekt
        :param config: dict - Konfigurationsdaten
        :return: None
        """
        super().__init__(master, config)

        # Titel hinzufügen
        self.create_dynamic_text("Rezept Suche", {"x": 150.0, "y": 18.0}, 20 * -1)

        # Gericht Suchfeld implementieren
        self.create_dynamic_text("Gericht", {"x": 18.0, "y": 52.0}, 15 * -1, "nw")

        self.create_entry({"x": 318.0, "y": 73.0, "width": 265.0, "height": 28.0})

        # Intoleranzen-Auswahl ermöglichen
        self.create_dynamic_text("Intoleranzen", {"x": 18.0, "y": 121.0}, 15 * -1, "nw")

        intolerances_de = []
        for key in self.config["intolerances"]:
            intolerances_de.append(key)

        self.create_multiselect_dropdown(
            name="intolerances",
            options=intolerances_de,
            position={"x": 18, "y": 147},
        )

        # Maximale Kalorienanzahl auswählbar machen
        self.create_dynamic_text(
            "Maximale Kalorien pro Portion", {"x": 18.0, "y": 197.0}, 15 * -1, "nw"
        )

        self.create_calorie_slider({"x": 18.0, "y": 245.0}, 0, 2000)

        # Enter Button integrieren
        self.create_button(
            "enter", lambda: self.search_recipes(), {"x": 150.0, "y": 310.0}
        )

        self.window.mainloop()

    def search_recipes(self):
        """Kombiniert die Eingaben und startet den Api-Request."""
        # Abrufen der Eingaben aus dem Such-Dashboard
        query = self.entry.get().lower()

        query = GoogleTranslator(source="auto", target="en").translate(query)

        dropdown_values = {}
        for name, data in self.dropdown_references.items():
            selected_values = [
                option
                for option, var in zip(data["options"], data["selected_vars"])
                if var.get()
            ]
            dropdown_values = selected_values

        intolerances = ",".join(
            [
                self.config["intolerances"][key]
                for key in dropdown_values
                if key in self.config["intolerances"]
            ]
        ).lower()

        calorie_value = None
        if "calorie_slider" in self.slider_references:
            calorie_value = self.slider_references["calorie_slider"][
                "calorie_value"
            ].get()

        # Request tätigen, wenn die Eingabe Sinn ergibt
        if len(query) <= 40 and re.match("^[a-zA-Z\\s]*$", query):
            input = {
                "query": query,
                "intolerances": intolerances,
                "maxCalories": calorie_value,
            }
            self.make_request(input)
            self.switch_to(ResultUi)
        else:
            self.show_error_dialog(
                "Bitte ein Gericht ohne Zahlen oder Sonderzeichen eingeben!"
            )
