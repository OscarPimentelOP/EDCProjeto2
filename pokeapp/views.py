from django.shortcuts import render

import pokeapp.queries as query
import re


# Create your views here.


def index(request):
    return render(request, 'index.html')


def pokemon(request, poke_id):
    pokemon_general_info_raw = query.pokeGlobalInfo(poke_id)
    pokemon_general_info_dict = {}
    pokemon_abilities_raw = query.getAbilityDescription(poke_id)
    pokemon_abilities_list = list()
    pokemon_weaknesses_raw = query.getPokemonWeaknesses(poke_id)
    pokemon_weaknesses_list = list()
    pokemon_strengths_raw = query.getPokemonStrengths(poke_id)
    pokemon_strengths_list = list()

    for elem in pokemon_general_info_raw['results']['bindings']:
        new_dict_val = elem['o']['value']
        new_dict_key = _get_last_word_from_url(elem['p']['value']).replace('-', '_')
        pokemon_general_info_dict[new_dict_key] = new_dict_val

    for elem in pokemon_abilities_raw['results']['bindings']:
        new_list_val = {'name': elem['oname']['value'],
                        'description': elem['desc']['value']}
        pokemon_abilities_list.append(new_list_val)

    for elem in pokemon_weaknesses_raw['results']['bindings']:
        pokemon_weaknesses_list.append(elem['weak']['value'])

    for elem in pokemon_strengths_raw['results']['bindings']:
        pokemon_strengths_list.append(elem['strong']['value'])

    print(pokemon_general_info_dict)

    tparams = {'general_info': pokemon_general_info_dict,
               'abilities': pokemon_abilities_list,
               'weaknesses': pokemon_weaknesses_list,
               'strengths': pokemon_strengths_list}
    return render(request, 'pokemon.html', tparams)


def _get_last_word_from_url(url_string):
    pattern = re.compile(r"\/([^\/]+)[\/]?$")
    return re.search(pattern, url_string).group(1)
