import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
import unittest

from src.utils import load_config
from ui.ui_base import UiBase

# Konfigurationsdaten laden
config_path = "config/settings.yml"
test_config = load_config(config_path)

# Konfigurationsdatei um Assets Pfad erweitern
assets_path = str(os.path.join(os.getcwd(), "ui/assets/"))
test_config.update({"assets_path": assets_path})


class UiBaseTest(unittest.TestCase):
    """Klasse um die UiBase-Klasse zu testen."""

    @classmethod
    def setUpClass(self):
        """Setup für die Tests."""
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
        self.ui_base = UiBase(self.root, test_config)
        self.ui_base.canvas = self.canvas

    @classmethod
    def tearDownClass(self):
        """Aufräumen nach den Tests."""
        self.root.quit()

    def test_create_button(self):
        """Teste die create_button Methode der UiBase-Klasse."""
        # simulieren
        self.ui_base.create_button(
            "enter", lambda: print("Button gedrückt!"), {"x": 150, "y": 150}
        )

        # überprüfen
        items = self.canvas.find_all()
        self.assertGreater(len(items), 0, "Kein Item im Canvas gefunden")
        self.assertTrue(
            any(self.canvas.type(item) == "image" for item in items),
            "Kein Image-Item im Canvas gefunden",
        )

    def test_create_entry(self):
        """Teste die create_entry Methode der UiBase-Klasse."""
        # simulieren
        self.ui_base.create_entry({"x": 100, "y": 100, "width": 200, "height": 30})

        # überprüfen
        entry_found = any(
            isinstance(child, tk.Entry) for child in self.root.winfo_children()
        )
        self.assertTrue(entry_found, "Kein Entry-Widget gefunden")

    def test_create_multiselect_dropdown(self):
        """Teste die create_multiselect_dropdown Methode der UiBase-Klasse."""
        # simulieren
        self.ui_base.create_multiselect_dropdown(
            "test_dropdown", ["Option 1", "Option 2"], {"x": 50, "y": 50}
        )

        # überprüfen
        label_found = any(
            isinstance(child, tk.Label) for child in self.canvas.winfo_children()
        )
        self.assertTrue(label_found, "Dropdown-Label wurde nicht gefunden")

    def test_create_calorie_slider(self):
        """Teste die create_calorie_slider Methode der UiBase-Klasse."""
        # simulieren
        self.ui_base.create_calorie_slider({"x": 100, "y": 150})

        # überprüfen
        slider_found = any(
            isinstance(child, tk.Scale) for child in self.canvas.winfo_children()
        )
        self.assertTrue(slider_found, "Slider-Widget wurde nicht gefunden")

    def test_create_dynamic_text(self):
        """Teste die create_dynamic_text Methode der UiBase-Klasse."""
        # simulieren
        self.ui_base.create_dynamic_text("Test Text", {"x": 100, "y": 100})

        # überprüfen
        text_found = any(
            self.canvas.type(item) == "text" for item in self.canvas.find_all()
        )
        self.assertTrue(text_found, "Text wurde nicht auf dem Canvas gefunden")

    def test_create_dynamic_image(self):
        """Teste die create_dynamic_image Methode der UiBase-Klasse."""
        # simulieren
        self.ui_base.create_dynamic_image(
            "https://www.w3schools.com/html/pic_trulli.jpg", {"x": 150, "y": 150}
        )

        # überprüfen
        image_found = any(
            self.canvas.type(item) == "image" for item in self.canvas.find_all()
        )
        self.assertTrue(image_found, "Bild wurde nicht auf dem Canvas gefunden")

    def test_switch_to(self):
        """Teste die switch_to Methode der UiBase-Klasse."""

        # Dashboard simulieren
        class MockDashboard(UiBase):
            def __init__(self, master, config):
                super().__init__(master, config)

        original_widget_count = len(self.root.winfo_children())
        self.ui_base.switch_to(MockDashboard)
        new_widget_count = len(self.root.winfo_children())

        # überprüfen
        self.assertNotEqual(
            original_widget_count,
            new_widget_count,
            "Das Dashboard wurde nicht gewechselt",
        )


if __name__ == "__main__":
    unittest.main()
