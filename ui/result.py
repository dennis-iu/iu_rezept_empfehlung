import importlib
from tkinter import PhotoImage

from ui.ui_base import UiBase


class ResultUi(UiBase):
    """Klasse für das Result-Dashboard."""

    def __init__(self, master, config):
        """
        Initialisieren der Klasse.

        :param master: tkinter objekt
        :param config: dict - Konfigurationsdaten
        :return: None
        """
        super().__init__(master, config)

        # Zurück Button integrieren
        search_module = importlib.import_module(
            "ui.search"
        )  # Um Circular Import Probleme zu verhindern
        SearchUi = search_module.SearchUi
        self.create_button(
            "back", lambda: self.switch_to(SearchUi), {"x": 12.0, "y": 11.0}, "nw"
        )

        # Refresh Button integrieren
        self.create_button(
            "refresh", lambda: self.refresh_result(), {"x": 259.0, "y": 7.0}, "nw"
        )

        # Rezept Namen integrieren
        self.create_dynamic_text(
            self.config["recipe"]["recipe_name"], {"x": 150, "y": 68.0}, 16 * -1
        )

        # Rezepte-Bild einfügen
        try:
            self.create_dynamic_image(
                self.config["recipe"]["recipe_img"], {"x": 150.0, "y": 140.0}
            )
        except:
            self.image_no_image_icon = PhotoImage(
                file=self.config["assets_path"] + "no_image_icon.png"
            )
            self.no_image_icon = self.canvas.create_image(
                150.0, 140.0, image=self.image_no_image_icon, anchor="center"
            )

        # Nährwerte anzeigen
        dynamic_y = 220
        for key, value in self.config["recipe"]["recipe_ntr"].items():
            self.create_dynamic_text(
                f"{key}: {value}", {"x": 150, "y": dynamic_y}, 14 * -1
            )
            dynamic_y += 15

        # Rezeptaufruf ermöglichen
        self.create_button(
            "rezept",
            lambda: self.open_link(self.config["recipe"]["recipe_url"]),
            {"x": 150.0, "y": 320.0},
        )

        self.window.mainloop()

    def refresh_result(self):
        """Methode um ein neues Rezept für die vorherige Anfrage angezeigt zu bekommen."""
        # Request mit höherem offset senden
        self.make_request(retry=True)

        # Dashboard neustarten
        self.switch_to(ResultUi)
