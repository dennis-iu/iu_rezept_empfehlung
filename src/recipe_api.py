"""
Class for Spoonacular API request.

Author:     Dennis Scholz
Created:    08.01.2025
Version:    1.0
"""

import logging as log
import re
import yaml
import requests

class RecipeApi():
    """Class for Spoonacular API source."""

    def __init__(self, config: dict):
        """
        Initialize the class.

        :param config: dict - Configuration dictionary
        :return: None
        """
        for key, value in config.items():
            setattr(self, key, value)
            print(key,value)
        
        # create headers for request
        self.headers = {"content_type": self.content_type,
                        "x-api-key": f"{self.api_key}"}
        
        # create list for relevant dashboard output
        self.dashboard_content = []

    def __enter__(self):
        """Enter the class."""
        self._request()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the class.

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

    def _request(self):
        """Send a request to the api."""
        payload = {
            'query': 'muffin',
            'diet': 'Vegetarian',
            'intolerances': 'Peanut',
            'number': 3,
            'instructionsRequired': True,
            'fillIngredients': True,
            'addRecipeInformation': True
        }
        try:
            response = requests.get(self.url, params=payload, headers=self.headers)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            log.error(f"Request to {self.url} failed: {e}")
            raise

    def prepare_data(self):
        """Prepare data for output."""
        for value in self.data["results"]:
            recipe = {
                "recipe_url": value["spoonacularSourceUrl"],
                "recipe_img": value["image"],
                "ingredients": []
            }

            for ingredient in value.get("extendedIngredients", []):
                recipe["ingredients"].append({
                "name": ingredient.get("nameClean"),
                "amount": ingredient["measures"]["metric"].get("amount"),
                "unit_short": ingredient["measures"]["metric"].get("unitShort"),
                "unit_long": ingredient["measures"]["metric"].get("unitLong"),
                })

            self.dashboard_content.append(recipe)

        log.info(self.dashboard_content)
