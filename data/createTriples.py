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
    triples_file.write('<http://edcpokedex.org/pokemon/%s> <http://edcpokedex.org/pred/art> %s .\n'
                       % (pokemon_json['id'], pokemon_json['sprites']['other']['official-artwork']['front_default']))


def convert_pokemon_to_triples(json_path, triples_file):
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


def convert_type_to_triples(triples_file):
    with open('csv/types.csv', 'r', encoding='utf-8') as types_csv:
        types_dict = csv.DictReader(types_csv)
        types_list = list()

        for type_row in types_dict:
            types_list.append(type_row['identifier'])

        for poke_type in types_list:
            triples_file.write('<http://edcpokedex.org/type/%s> '
                               '<http://edcpokedex.org/pred/name> '
                               '"%s" .\n' % (poke_type, poke_type.capitalize()))

            with open('csv/type_efficacy.csv', 'r', encoding='utf-8') as types_efficacy_csv:
                types_efficacy_dict = csv.DictReader(types_efficacy_csv)

                for efficacy_row in types_efficacy_dict:
                    if types_list[int(efficacy_row['damage_type_id']) - 1] == poke_type:
                        if int(efficacy_row['damage_factor']) > 100:
                            triples_file.write('<http://edcpokedex.org/type/%s> '
                                               '<http://edcpokedex.org/pred/isSuperEffective> '
                                               '<http://edcpokedex.org/type/%s> .\n'
                                               % (poke_type, types_list[int(efficacy_row['target_type_id']) - 1]))
                        elif int(efficacy_row['damage_factor']) < 100:
                            triples_file.write('<http://edcpokedex.org/type/%s> '
                                               '<http://edcpokedex.org/pred/isWeak> '
                                               '<http://edcpokedex.org/type/%s> .\n'
                                               % (poke_type, types_list[int(efficacy_row['target_type_id']) - 1]))


def convert_abilities_to_triples(triples_file):
    abilities_list = list()
    abilities_names_list = list()
    abilities_flavor_list = list()

    with open("csv/abilities.csv", 'r', encoding='utf-8') as abilities_csv:
        abilities_dict = csv.DictReader(abilities_csv)
        for row in abilities_dict:
            if int(row['id']) < 10000:
                abilities_list.append(row['identifier'])

    with open("csv/ability_names.csv", 'r', encoding='utf-8') as abilities_names_csv:
        abilities_names_dict = csv.DictReader(abilities_names_csv)
        for row in abilities_names_dict:
            if int(row['ability_id']) < 10000:
                if row['local_language_id'] == language_id:
                    abilities_names_list.append(row['name'])

    with open("csv/ability_flavor_text.csv", 'r', encoding='utf-8') as abilities_flavor_csv:
        abilities_flavor_dict = csv.DictReader(abilities_flavor_csv)
        for row in abilities_flavor_dict:
            if row['version_group_id'] == '18' or row['version_group_id'] == '20':
                if row['language_id'] == language_id:
                    abilities_flavor_list.append(row['flavor_text'])

    count = 0

    for ability in abilities_list:
        triples_file.write('<http://edcpokedex.org/ability/%s> '
                           '<http://edcpokedex.org/pred/name> '
                           '"%s" .\n'
                           % (ability, abilities_names_list[count]))
        triples_file.write('<http://edcpokedex.org/ability/%s> '
                           '<http://edcpokedex.org/pred/description> '
                           '"%s" .\n'
                           % (ability, abilities_flavor_list[count]))
        count += 1


if __name__ == '__main__':
    #with open('triples/pokemon.nt', 'w', encoding='utf-8') as poke_triples:
    #    for file in os.scandir("json/pokemon"):
    #        if file.path.endswith(".json"):
    #            convert_pokemon_to_triples(file.path, poke_triples)

    with open('triples/types.nt', 'w', encoding='utf-8') as type_triples:
        convert_type_to_triples(type_triples)

    with open('triples/abilities.nt', 'w', encoding='utf-8') as ability_triples:
        convert_abilities_to_triples(ability_triples)
