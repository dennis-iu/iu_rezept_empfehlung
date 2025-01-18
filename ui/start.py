import logging as log

from ui.key_entry import KeyEntryUi
from ui.search import SearchUi
from ui.ui_base import UiBase


class StartUi(UiBase):
    """Klasse für das Start-Dashboard."""

    def __init__(self, master, config):
        """
        Initialisieren der Klasse.

        :param master: tkinter objekt
        :param config: dict - Konfigurationsdaten
        :return: None
        """
        super().__init__(master, config)

        # Willkommens-Text integrieren
        self.create_dynamic_text("Willkommen", {"x": 150.0, "y": 152.0}, 40 * -1)

        # Start-Button integrieren
        self.create_button(
            "start", lambda: self.choose_next_ui(), {"x": 150.0, "y": 236.0}
        )

        self.window.mainloop()

    def choose_next_ui(self):
        """Methode um die nächste Ui zu starten."""
        if self.config["headers"].get("x-api-key", None) is None:
            log.info("Keinen Api-Key gefunden, starte Key_Entry-Dashboard.")
            self.switch_to(KeyEntryUi)
        else:
            log.info("Api-Key gefunden, starte Such-Dashboard.")
            self.switch_to(SearchUi)
