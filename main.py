import logging as log
from src.recipe_api import RecipeApi
from src.utils import (load_config, set_api_key)

# log-config
log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def main():
    """Main function to start the recipe app."""
    # get config for api request
    config_path = 'config/settings.yml'
    config = load_config(config_path)

    # get api_key from gitignore file
    api_key_path = 'config/api_key.yml'
    config.update(set_api_key(api_key_path))

    log.info("Successfully loaded config!")
    
    with RecipeApi(config) as ra:
        # prepare data for output
        ra.prepare_data()

if __name__ == "__main__":
    main()