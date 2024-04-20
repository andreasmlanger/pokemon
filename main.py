"""
Downloads Pokémon images and information from the web, then uploads it to the database
"""

from dotenv import load_dotenv
import os
from data.download import fetch_pokemon_data_from_wikipedia, download_pokemon_images_and_create_json
from data.upload import drop_all_tables, upload_pokemon_json_to_database

load_dotenv()

IMAGE_DIR = os.path.join('assets', 'images')
JSON_PATH = os.path.join('assets', 'pokemon.json')


def main():
    # poke_dic = fetch_pokemon_data_from_wikipedia()
    # download_pokemon_images_and_create_json(poke_dic, image_dir=IMAGE_DIR, json_path=JSON_PATH)
    # drop_all_tables()  # will reset the complete PostgreSQL database!
    upload_pokemon_json_to_database(json_path=JSON_PATH)


if __name__ == '__main__':
    main()
