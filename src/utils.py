import yaml
import os
import logging as log

def load_config(file_path):
    """
    Loads yaml and returns it as dict.
    
    :param file_path: string - config yaml path
    :return: dict
    """
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        log.warning(f"Couldn't read config yaml file. Exception: {e}")
    
def set_api_key(key_path):
    """
    Checks for api_key and returns it.
    
    :param key_path: string - api_key yaml path
    :return: dict
    """
    if os.path.exists(key_path):
        try:
            with open(key_path, "r") as file:
                api_key_dict = yaml.safe_load(file)
                if not api_key_dict["api_key"]:
                    log.info("No key in file.")
                    api_key_dict = cc_key_file(key_path)
                return api_key_dict
        except yaml.YAMLError as e:
            log.warning(f"Couldn't read api_key yaml file. Exception: {e}")
    else:
        log.info("No key file found in path!")
        api_key_dict = cc_key_file(key_path)
        return api_key_dict

    
def cc_key_file(key_path):
    """
    Creates or Changes yaml file for api_key.

    :param key_path: string - key_path
    :return: dict
    """
    try:
        api_key_dict = {}
        api_key = input("Please Input your spoonacular api key here: ").strip()
        api_key_dict = {"api_key": str(api_key)}
        with open(key_path, "w") as file:
            yaml.dump(api_key_dict, file)
            log.info(f"Key has been added to {key_path}.")
        return api_key_dict
    except Exception as e:
        log.error("Could'nt create or change yaml file for api key.")