"""
Scripts to download Pokémon images and information from the web
"""

from bs4 import BeautifulSoup
import requests
import json
import os
import re


BASE_URL = 'https://pokemon.gameinfo.io'  # website with Pokémon info

# Exclude these forms from download
BLACK_LIST_CONTAINS = ('2019', '2020', '2021', '2022', '2023', '2024', 'armored')
BLACK_LIST_IN = ('s', 'oh-s')
BLACK_LIST_IDX = (25, 493, 649, 664, 665)  # e.g. all Pikachu costumes


def fetch_pokemon_data_from_wikipedia():
    url = 'https://en.wikipedia.org/wiki/List_of_Pokémon'
    soup = get_soup(url)
    table = soup.find_all('table')[2]  # information about Pokémon is stored in second table on page
    tds = table.find_all('td')
    pokemon_list = [td.get_text(strip=True) for td in tds]
    pokemon_dic = create_pokemon_dictionary_from_list(pokemon_list)
    return pokemon_dic


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def create_pokemon_dictionary_from_list(pokemon_list):
    pokemon_dic = {}
    for i in range(len(pokemon_list)):
        if pokemon_list[i].isdigit():
            poke_index = int(pokemon_list[i])
            poke_name = re.sub(r'[^a-zA-Z]', '', pokemon_list[i + 1])  # name is stored in next cell
            pokemon_dic[poke_index] = poke_name
    return pokemon_dic


def download_pokemon_images_and_create_json(poke_dic, image_dir, json_path):
    poke_list = []
    for (poke_index, poke_name) in sorted(poke_dic.items()):
        string_index = str(poke_index).zfill(4)

        # Scrape page of Pokémon
        url = f'{BASE_URL}/en/pokemon/{poke_index}-{poke_name}'
        soup = get_soup(url)

        if not page_exists(soup):
            continue

        # Find available forms
        forms = find_forms(soup, idx=poke_index)

        for form in forms:
            if form:
                soup = get_soup(f'{url}/{form}')  # get soup from additional form
                form = format_form(form)

            bg_type = download_bg_image(soup, image_dir=image_dir)  # download background image
            success = download_pokemon_image(soup, string_index, form, image_dir=image_dir)  # download Pokémon image

            if success:
                poke_info = {'idx': poke_index, 'name': poke_name, 'type': bg_type}
                if form:
                    poke_info.update({'form': form})
                    print(f'{string_index}: {poke_name} ({form})')
                else:
                    print(f'{string_index}: {poke_name}')
                poke_list.append(poke_info)  # append information to poke_list

    save_to_json(poke_list, json_path=json_path)


def download_bg_image(soup, image_dir):
    bg_element = soup.find('div', class_='bg')
    style_attribute = bg_element.get('style')
    bg_img_url = style_attribute.split('url(')[1].split(')')[0]
    bg_type = bg_img_url.replace('/images/game/details_type_bg_', '').replace('.png', '')
    download_image(f'{BASE_URL}{bg_img_url}', file_name=f'{bg_type}.png', image_dir=image_dir)  # e.g. 'steel.png'
    return bg_type


def download_pokemon_image(soup, string_index, form, image_dir):
    meta_tag = soup.find('meta', property='og:image')
    img_url = meta_tag['content']
    return download_image(img_url, file_name=f'{string_index}_{form}.png'.replace('_.', '.'), image_dir=image_dir)


def download_image(img_url, file_name, image_dir):
    file_path = os.path.join(image_dir, file_name)
    if os.path.isfile(file_path):
        return True  # image is already there
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return True  # image successfully downloaded


def save_to_json(poke_list, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(poke_list, json_file, indent=2)


def find_forms(soup, idx):
    select_tag = soup.find('select', id='forms')
    if select_tag and idx not in BLACK_LIST_IDX:
        options = select_tag.find_all('option')
        option_values = [option['value'] for option in options]
        forms = []
        for value in option_values:
            form = value.split('/')[-1]
            if any(s in form for s in BLACK_LIST_CONTAINS) or form in BLACK_LIST_IN:
                continue
            elif str(idx) in form:
                forms.append('')  # normal form
            else:
                forms.append(form)
        return forms
    return ['']  # only normal form


def page_exists(soup):
    title_tag = soup.find('title')  # check title to see if page exists
    return title_tag and '404' not in title_tag.get_text()


def format_form(form):
    return form.replace('-form', '').replace('-evolution', '').replace('evolution-primal', '').replace('mime-', '')
