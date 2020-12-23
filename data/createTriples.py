import json
import csv
import os

# English Language ID in PokeAPI
language_id = '9'


def write_pokemon_names(pokemon_json, triples_file):
    triples_file.write('<http://edcpokedex.org/pokemon/%s> '
                       '<http://edcpokedex.org/pred/name> '
                       '"%s" .\n'
                       % (pokemon_json['id'], pokemon_json['name'].capitalize()))


def write_pokemon_description(pokemon_json, triples_file):
    with open('csv/pokemon_species_flavor_text.csv', 'r', encoding='utf-8') as poke_desc_csv:
        poke_desc_dict = csv.DictReader(poke_desc_csv)
        for row in poke_desc_dict:
            if str(row['species_id']) == str(pokemon_json['id']):
                if row['language_id'] == language_id:
                    triples_file.write('<http://edcpokedex.org/pokemon/%s> '
                                       '<http://edcpokedex.org/pred/description> '
                                       '"%s" .\n'
                                       % (pokemon_json['id'], row['flavor_text'].replace('\n', ' ').replace('', ' ')))
                    break


def write_pokemon_height_weight(pokemon_json, triples_file):
    triples_file.write('<http://edcpokedex.org/pokemon/%s> '
                       '<http://edcpokedex.org/pred/height> '
                       '"%s" .\n'
                       % (pokemon_json['id'], pokemon_json['height']))

    triples_file.write('<http://edcpokedex.org/pokemon/%s> '
                       '<http://edcpokedex.org/pred/weight> '
                       '"%s" .\n'
                       % (pokemon_json['id'], pokemon_json['weight']))


def write_pokemon_category(pokemon_json, triples_file):
    with open('csv/pokemon_species_names.csv', 'r', encoding='utf-8') as poke_cat_csv:
        poke_cat_dict = csv.DictReader(poke_cat_csv)
        for row in poke_cat_dict:
            if str(row['pokemon_species_id']) == str(pokemon_json['id']):
                if row['local_language_id'] == language_id:
                    poke_cat_split = row['genus'].split(' Pokémon')
                    poke_cat = poke_cat_split[0].replace(' ', '-').lower()
                    triples_file.write(
                        '<http://edcpokedex.org/pokemon/%s> '
                        '<http://edcpokedex.org/pred/category> '
                        '<http://edcpokedex.org/category/%s> .\n' % (
                            pokemon_json['id'], poke_cat))
                    break


def write_pokemon_ability(pokemon_json, triples_file):
    for ability in pokemon_json['abilities']:
        triples_file.write('<http://edcpokedex.org/pokemon/%s> '
                           '<http://edcpokedex.org/pred/ability> '
                           '<http://edcpokedex.org/ability/%s> .\n'
                           % (pokemon_json['id'], ability['ability']['name']))


def write_pokemon_type(pokemon_json, triples_file):
    for poke_type in pokemon_json['types']:
        triples_file.write('<http://edcpokedex.org/pokemon/%s> '
                           '<http://edcpokedex.org/pred/type> '
                           '<http://edcpokedex.org/type/%s> .\n'
                           % (pokemon_json['id'], poke_type['type']['name']))


def write_pokemon_stats(pokemon_json, triples_file):
    for stat in pokemon_json['stats']:
        triples_file.write('<http://edcpokedex.org/pokemon/%s> '
                           '<http://edcpokedex.org/pred/%s> '
                           '"%s" .\n' % (pokemon_json['id'], stat['stat']['name'], stat['base_stat']))


def write_pokemon_evolutions(pokemon_json, triples_file):
    with open('csv/pokemon_evolution.csv', 'r', encoding='utf-8') as poke_evo_csv:
        poke_evo_dict = csv.DictReader(poke_evo_csv)
        for row in poke_evo_dict:
            if str(row['id']) == str(pokemon_json['id']):
                triples_file.write('<http://edcpokedex.org/pokemon/%s> '
                                   '<http://edcpokedex.org/pred/evolves-to> '
                                   '<http://edcpokedex.org/pokemon/%s> .\n'
                                   % (pokemon_json['id'], row['evolved_species_id']))
                break


def write_pokemon_official_art(pokemon_json, triples_file):
    triples_file.write('<http://edcpokedex.org/pokemon/1> <http://edcpokedex.org/pred/art> %s .\n'
                       % (pokemon_json['sprites']['other']['official-artwork']['front_default']))


def convert_to_triples(json_path, triples_file):
    with open(json_path) as pokemon_json_file:
        pokemon_json = json.load(pokemon_json_file)
        write_pokemon_names(pokemon_json, triples_file)
        write_pokemon_description(pokemon_json, triples_file)
        write_pokemon_height_weight(pokemon_json, triples_file)
        write_pokemon_category(pokemon_json, triples_file)
        write_pokemon_ability(pokemon_json, triples_file)
        write_pokemon_type(pokemon_json, triples_file)
        write_pokemon_stats(pokemon_json, triples_file)
        write_pokemon_evolutions(pokemon_json, triples_file)
        write_pokemon_official_art(pokemon_json, triples_file)


if __name__ == '__main__':
    with open('triples/pokemon.nt', 'w', encoding='utf-8') as poke_triples:
        for file in os.scandir("json/pokemon"):
            if file.path.endswith(".json"):
                convert_to_triples(file.path, poke_triples)
