"""
Klasse für Spoonacular API request.

Author:     Dennis Scholz
Created:    08.01.2025
Version:    1.0
"""

import logging as log

import requests
from deep_translator import GoogleTranslator


class RecipeApi:
    """Klasse für die Spoonacular API Quelle."""

    def __init__(self, config: dict):
        """
        Klasse initialisieren.

        :param config: dict - Konfigurationsdaten
        :return: None
        """
        for key, value in config.items():
            setattr(self, key, value)

    def __enter__(self):
        """Klasse öffnen."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Klasse verlassen.

        :param exc_type: Exception Type
        :param exc_val: Exception Value
        :param exc_tb: Exception Traceback
        :return: None
        """
        if exc_type is not None:
            log.error(f"Exception: {exc_type} - {exc_val}")
            log.error(
                f"Traceback: {exc_tb.tb_frame.f_code.co_filename} - {exc_tb.tb_lineno}"
            )
            raise exc_val

    def send_request(self):
        """
        Request an die Api senden.

        :return: list: Ergebnis
        """
        try:
            response = requests.get(self.url, params=self.payload, headers=self.headers)
            response.raise_for_status()
            self.data = {}
            self.data = response.json()
            self.get_nutritional_information()
            self.prepare_data()
            return self.recipe
        except requests.exceptions.RequestException as e:
            log.error(f"Request zur {self.url} fehlgeschlagen. Exception: {e}")
            raise

    def get_nutritional_information(self):
        """Funktion um zusätzliche Information zu den Kalorien zu bekommen."""
        url_part_1 = "https://api.spoonacular.com/recipes/"
        nutrition_url = (
            url_part_1 + f"{self.data["results"][0]["id"]}/nutritionWidget.json"
        )
        response = requests.get(nutrition_url, headers=self.headers)
        response.raise_for_status()
        self.data.update(response.json())

    def prepare_data(self):
        """Daten für die Ergebnisanzeige vorbereiten."""
        # Namen übersetzen
        recipe_name = GoogleTranslator(source="auto", target="de").translate(
            self.data["results"][0]["title"]
        )

        # Ablegen der Standardangaben
        self.recipe = {}
        self.recipe = {
            "recipe_name": recipe_name,
            "recipe_img": self.data["results"][0]["image"],
            "recipe_url": self.data["results"][0]["spoonacularSourceUrl"],
            "recipe_ntr": {},
        }

        # Ablegen der Nährwerte
        relevant_nutrients = ["Calories", "Fat", "Carbohydrates", "Protein"]
        for item in self.data["nutrients"]:
            if item["name"] in relevant_nutrients:
                item_name_de = GoogleTranslator(source="auto", target="de").translate(
                    item["name"]
                )
                self.recipe["recipe_ntr"].update(
                    {f"{item_name_de}": f"{item["amount"]} {item["unit"]}"}
                )
