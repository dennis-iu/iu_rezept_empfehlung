import logging as log
import os

import yaml


def load_config(file_path):
    """
    Lädt yaml-Datei und gibt sie in einem dictionary zurück.

    :param file_path: string - Konfig-Yaml-Pfad
    :return: dict
    """
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        log.warning(f"Konnte Yaml-Pfad nicht auslesen. Exception: {e}")


def set_api_key(key_path):
    """
    Prüft ob es einen api-key gibt und setzt ihn.

    :param key_path: string - Api-Key-Yaml-Pfad
    :return: dict or message
    """
    api_key_dict = {}
    if os.path.exists(key_path):
        try:
            with open(key_path, "r") as file:
                api_key_dict = yaml.safe_load(file)
                if not api_key_dict["api_key"]:
                    log.warning("Konnte keinen Api-Key in der Yaml finden.")
                return api_key_dict["api_key"]
        except yaml.YAMLError as e:
            log.warning(f"Konnte die Api-Key-Yaml Datei nicht auslesen. Exception: {e}")
    else:
        log.warning("Keine Api-Key-Yaml gefunden!")
        return api_key_dict


def save_api_key(api_key):
    """
    Speichert Api-Key in einer Yaml.

    :param api_key: string - api_key
    :return: None
    """
    try:
        api_key_dict = {"api_key": api_key}
        api_key_path = "config/api_key.yml"
        with open(api_key_path, "w") as file:
            yaml.dump(api_key_dict, file)
            log.info(f"Key wurde in diesem Pfad gespeichert: {api_key_path}.")
    except Exception:
        log.error("Konnte den Key nicht speichern. Exception: {e}")
