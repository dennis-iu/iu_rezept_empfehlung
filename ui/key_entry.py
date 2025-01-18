from tkinter import messagebox

from src.utils import save_api_key
from ui.search import SearchUi
from ui.ui_base import UiBase


class KeyEntryUi(UiBase):
    """Klasse für das Key_Entry-Dashboard."""

    def __init__(self, master, config):
        """
        Initialisieren der Klasse.

        :param master: tkinter objekt
        :param config: dict - Konfigurationsdaten
        :return: None
        """
        super().__init__(master, config)

        # Api-Key Eingabe Text
        self.create_dynamic_text("API-KEY Eingabe", {"x": 150.0, "y": 152.0}, 20 * -1)

        # Eingabefenster integrieren
        self.create_entry({"x": 318.0, "y": 180.0, "width": 265.0, "height": 28.0})

        # Enter Button integrieren
        self.create_button("enter", lambda: self.save_key(), {"x": 150.0, "y": 236.0})

        # Key bekommen Button integrieren
        self.create_button(
            "key_bekommen",
            lambda: self.open_link(
                "https://spoonacular.com/food-api/console#Dashboard"
            ),
            {"x": 150.0, "y": 293.0},
        )

        self.window.mainloop()

    def save_key(self):
        """Methode um den Input als Api_Key zu speichern."""
        api_key = self.entry.get()
        if len(api_key) >= 20 and api_key.isalnum():
            self.config["headers"].update({"x-api-key": api_key})
            save_api_key(api_key)
            messagebox.showinfo("Erfolg", "API Key gespeichert!")
            self.switch_to(SearchUi)
        else:
            self.show_error_dialog("Bitte einen gültigen API Key eingeben!")
