import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import unittest
from unittest.mock import MagicMock, patch

from recipe_api import RecipeApi
from utils import load_config, set_api_key


class RecipeApiTest(unittest.TestCase):
    """Klasse um die RecipeApi-Klasse zu testen."""

    def setUp(self):
        """Setup für die Tests."""
        # Konfigurationsdaten laden
        config_path = "config/settings.yml"
        self.config = load_config(config_path)

        # api_key über gitignore Datei holen
        api_key_path = "config/api_key.yml"
        self.config["headers"].update({"x-api-key": set_api_key(api_key_path)})

        # Beispiel payload anwenden
        self.config["payload"].update(
            {"query": "muffin", "intolerances": "peanut", "maxCalories": "700"}
        )
        self.recipe_api = RecipeApi(self.config)

    @patch("recipe_api.requests.get")
    @patch("recipe_api.GoogleTranslator.translate")
    def test_api_integration(self, mock_translate, mock_get):
        """Test der Gesamtfunktionalität der API-Klasse."""
        # Mocking der API-Antwort
        mock_search_response = MagicMock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = {
            "results": [
                {
                    "id": 12345,
                    "title": "Delicious Muffin",
                    "image": "http://example.com/image.jpg",
                    "spoonacularSourceUrl": "http://example.com/recipe",
                }
            ]
        }

        # Mocking der Nährwerte-Antwort
        mock_nutrition_response = MagicMock()
        mock_nutrition_response.status_code = 200
        mock_nutrition_response.json.return_value = {
            "nutrients": [
                {"name": "Calories", "amount": 200, "unit": "kcal"},
                {"name": "Fat", "amount": 10, "unit": "g"},
                {"name": "Carbohydrates", "amount": 30, "unit": "g"},
                {"name": "Protein", "amount": 5, "unit": "g"},
            ]
        }

        # Mocking der Antworten in einer Liste
        mock_get.side_effect = [mock_search_response, mock_nutrition_response]

        # Mocking vom GoogleTranslator mit Übersetzungen
        def translate_side_effect(text):
            """
            Methode um die Übersetzungen zu mocken.

            :param text: str - Zu übersetzender Text
            :return: str - Übersetzung
            """
            translations = {
                "Delicious Muffin": "Leckere Muffins",
                "Calories": "Kalorien",
                "Fat": "Fett",
                "Carbohydrates": "Kohlenhydrate",
                "Protein": "Protein",
            }
            return translations.get(text, text)

        mock_translate.side_effect = translate_side_effect

        # API-Aufruf testen
        result = self.recipe_api.send_request()

        # Überprüfung der Rückgabedaten
        expected_result = {
            "recipe_name": "Leckere Muffins",
            "recipe_img": "http://example.com/image.jpg",
            "recipe_url": "http://example.com/recipe",
            "recipe_ntr": {
                "Kalorien": "200 kcal",
                "Fett": "10 g",
                "Kohlenhydrate": "30 g",
                "Protein": "5 g",
            },
        }
        self.assertEqual(result, expected_result)

    def tearDown(self):
        """Aufräumen nach den Tests."""
        del self.recipe_api


if __name__ == "__main__":
    unittest.main()
