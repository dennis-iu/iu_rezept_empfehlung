import logging as log
import os

from src.utils import load_config, set_api_key
from ui.start import StartUi

try:
    import tkinter as tk
except ImportError:
    raise ImportError("tkinter ist nicht installiert.")

# log-config
log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    """Main Funktion zum starten der Rezepte-Anwendung."""
    # Konfigurationsdaten laden
    config_path = "config/settings.yml"
    config = load_config(config_path)

    # Konfigurationsdatei um Assets Pfad erweitern
    assets_path = str(os.path.join(os.getcwd(), "ui/assets/"))
    config.update({"assets_path": assets_path})

    # api_key über gitignore Datei holen
    api_key_path = "config/api_key.yml"
    config["headers"].update({"x-api-key": set_api_key(api_key_path)})

    log.info("Konfigurationsdatei geladen.")

    # Tkinter root initialisieren
    root = tk.Tk()

    # Starte das erste Dashboard
    with StartUi(root, config):
        log.info("Dashboard gestartet!")

    root.mainloop()


if __name__ == "__main__":
    main()
