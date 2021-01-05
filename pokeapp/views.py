from django.shortcuts import render
from django.template.defaulttags import register

import pokeapp.queries as query
import re


# Create your views here.


def index(request):
    pokemon_list_raw = query.listPokedex()
    pokemon_list = []

    for elem in pokemon_list_raw['results']['bindings']:
        pokemon_list.append((elem['id']['value'], elem['name']['value'], elem['art']['value']))

    tparams = {
        'pokemon_list': pokemon_list
    }
    return render(request, 'pokedex.html', tparams)


def pokemon(request, poke_id):
    pokemon_general_info_raw = query.pokeGlobalInfo(poke_id)
    pokemon_general_info_dict = {}
    pokemon_type_raw = query.getPokemonType(poke_id)
    pokemon_type_list = list()
    pokemon_category_raw = query.getPokemonCategory(poke_id)
    pokemon_category = ""
    pokemon_abilities_raw = query.getAbilityDescription(poke_id)
    pokemon_abilities_list = list()
    pokemon_weaknesses_raw = query.getPokemonWeaknesses(poke_id)
    pokemon_weaknesses_list = list()
    pokemon_strengths_raw = query.getPokemonStrengths(poke_id)
    pokemon_strengths_list = list()
    pokemon_evolutions_raw = query.getEvolutionLine(poke_id)
    pokemon_evolutions_dict = {'first': [], 'second': [], 'third': []}

    for elem in pokemon_general_info_raw['results']['bindings']:
        new_dict_val = elem['o']['value']
        new_dict_key = _get_last_word_from_url(elem['p']['value']).replace('-', '_')
        pokemon_general_info_dict[new_dict_key] = new_dict_val

    for elem in pokemon_type_raw['results']['bindings']:
        pokemon_type_list.append(elem['typename']['value'])

    for elem in pokemon_category_raw['results']['bindings']:
        pokemon_category = elem['categoryname']['value']

    for elem in pokemon_abilities_raw['results']['bindings']:
        new_list_val = {'name': elem['abilityname']['value'],
                        'description': elem['description']['value']}
        pokemon_abilities_list.append(new_list_val)

    for elem in pokemon_weaknesses_raw['results']['bindings']:
        pokemon_weaknesses_list.append(elem['weak']['value'])

    for elem in pokemon_strengths_raw['results']['bindings']:
        pokemon_strengths_list.append(elem['strong']['value'])

    if poke_id != 133:
        first_evo = _get_pokemon_name_and_image(pokemon_evolutions_raw[0])
        if len(pokemon_evolutions_raw) > 1:
            second_evo = _get_pokemon_name_and_image(pokemon_evolutions_raw[1])
            pokemon_evolutions_dict['second'].append(second_evo)
        if len(pokemon_evolutions_raw) > 2:
            third_evo = _get_pokemon_name_and_image(pokemon_evolutions_raw[2])
            pokemon_evolutions_dict['third'].append(third_evo)

        pokemon_evolutions_dict['first'].append(first_evo)
    else:
        first_evo = _get_pokemon_name_and_image(pokemon_evolutions_raw[0])
        pokemon_evolutions_dict['first'].append(first_evo)

        for poke in pokemon_evolutions_raw[1:]:
            second_evo = _get_pokemon_name_and_image(poke)
            pokemon_evolutions_dict['second'].append(second_evo)

    tparams = {'general_info': pokemon_general_info_dict,
               'category': pokemon_category,
               'types': pokemon_type_list,
               'abilities': pokemon_abilities_list,
               'weaknesses': pokemon_weaknesses_list,
               'strengths': pokemon_strengths_list,
               'evolutions': pokemon_evolutions_dict}
    return render(request, 'pokemon.html', tparams)


def about(request):
    pokemon_info_raw = query.get_dbpedia_pokemon_desc_and_pic()

    pokemon_game_info_raw = query.get_dbpedia_pokemon_game_list()
    pokemon_game_info_dict = {}

    for elem in pokemon_game_info_raw['results']['bindings']:
        game_name = elem['gamename']['value']
        if game_name not in pokemon_game_info_dict:
            pokemon_game_info_dict[game_name] = {"consoles": []}

        console_name = _get_last_word_from_url(elem['platform']['value']).replace("_", " ")
        pokemon_game_info_dict[game_name]["consoles"].append(console_name)

    tparams = {'pk_logo': pokemon_info_raw['results']['bindings'][0]['thumbnail']['value'],
               'pk_desc': pokemon_info_raw['results']['bindings'][0]['abstract']['value'],
               'pk_games': pokemon_game_info_dict}

    return render(request, 'about.html', tparams)


def _get_last_word_from_url(url_string):
    pattern = re.compile(r"\/([^\/]+)[\/]?$")
    return re.search(pattern, url_string).group(1)


def _get_pokemon_name_and_image(poke_id):
    raw_res = query.getPokemonPicAndName(poke_id)
    res = dict.fromkeys(['id', 'name', 'art'])
    res['id'] = poke_id

    for elem in raw_res['results']['bindings']:
        res['name'] = elem['poke_name']['value']
        res['art'] = elem['poke_art']['value']

    return res


# from stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
