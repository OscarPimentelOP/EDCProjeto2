from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

import pokeapp.queries as query
import re
import json


# Create your views here.


def index(request):
    poke_type = request.GET.get('type', '')
    search = request.GET.get('search', '')
    page_num = request.GET.get('page', 1)

    if poke_type and search:
        pokemon_list_raw = query.searchListPokemonFromType(poke_type, search)
    elif poke_type:
        pokemon_list_raw = query.listPokemonFromType(poke_type)
    elif search:
        pokemon_list_raw = query.search(search)
    else:
        pokemon_list_raw = query.listPokedex()

    pokemon_list = []

    for elem in pokemon_list_raw['results']['bindings']:
        pokemon_list.append((int(elem['id']['value']), elem['name']['value'], elem['art']['value']))

    pokemon_list.sort(key=lambda pokemon : pokemon[0])
    pokemon_paginator = Paginator(pokemon_list, 40)
    print(pokemon_paginator.num_pages)

    tparams = {
        'pokemon_list': pokemon_paginator.page(page_num),
        'types': ['Normal', 'Fire', 'Fighting', 'Water', 'Flying', 'Grass',
                  'Poison', 'Electric', 'Ground', 'Psychic', 'Rock', 'Ice',
                  'Bug', 'Dragon', 'Ghost', 'Dark', 'Steel', 'Fairy']
    }
    return render(request, 'pokedex.html', tparams)


def pokemonapi(request):
    pokemon_list_raw = query.listPokedex()
    pokemon_dictionary = {}

    for elem in pokemon_list_raw['results']['bindings']:
        pokemon_dictionary[elem['id']['value']] = {'name': elem['name']['value'], 'art': elem['art']['value']}

    return JsonResponse(pokemon_dictionary)


def get_details(request):
    if request.method == "GET":
        ret_dict = {}

        if 'team-pokemons' in request.GET.keys():

            id_list = request.GET['team-pokemons'].strip('][').split(',')

            for pokemon_id in id_list:
                types = query.getPokemonType(pokemon_id)
                pokemon_types = []

                for pok_type in types['results']['bindings']:
                    pokemon_types.append(pok_type['typename']['value'])

                if len(pokemon_types) > 1:
                    ret_dict[pokemon_id] = query.getCompleteChart(pokemon_types[0], pokemon_types[1])
                else:
                    ret_dict[pokemon_id] = query.getCompleteChart(pokemon_types[0])

            return JsonResponse(ret_dict)

        else:
            return JsonResponse({"status": False})


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

    for pokemon_id in pokemon_evolutions_raw['firstStage']:
        evo = _get_pokemon_name_and_image(pokemon_id)
        pokemon_evolutions_dict['first'].append(evo)

    for pokemon_id in pokemon_evolutions_raw['secondStage']:
        evo = _get_pokemon_name_and_image(pokemon_id)
        pokemon_evolutions_dict['second'].append(evo)

    for pokemon_id in pokemon_evolutions_raw['thirdStage']:
        evo = _get_pokemon_name_and_image(pokemon_id)
        pokemon_evolutions_dict['third'].append(evo)

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


def teams(request):
    teams_list_raw = query.listAllTeams()
    teams_dict = {}

    for elem in teams_list_raw['results']['bindings']:
        if elem['teamName']['value'] not in teams_dict.keys():
            teams_dict[elem['teamName']['value']] = []
        teams_dict[elem['teamName']['value']].append((elem['id']['value'], elem['name']['value'], elem['art']['value']))

    tparams = {
        'teams_dict': teams_dict
    }

    return render(request, "teams.html", tparams)


def team(request, team_name):
    team_data_raw = query.listTeamsAndPokemon(team_name)
    team_pokemons = []

    for elem in team_data_raw['results']['bindings']:
        team_pokemons.append((elem['id']['value'], elem['name']['value'], elem['art']['value']))

    tparams = {
        'team_name': team_name,
        'team_pokemon': team_pokemons
    }
    return render(request, "team.html", tparams)


def create_team(request):
    if request.method == "POST":
        if 'name' in request.POST and 'team-pokemons' in request.POST:
            name = request.POST.get('name').replace(' ', '_')
            is_created = query.createNewTeam(name)

            if is_created:
                id_list = request.POST['team-pokemons'].strip('][').split(',')
                for pokemon_id in id_list:
                    query.insertPokeInTeam(pokemon_id, request.POST.get('name'))

                return JsonResponse({'status': True})

    return JsonResponse({'status': False})


def delete_team(request):
    if request.method == "POST":
        if 'name' in request.POST:
            name = request.POST.get('name').replace(' ', '_')
            if query.checkTeamExists(name)['boolean']:
                query.deleteTeam(request.POST.get('name'))
                return JsonResponse({'status': True})

    return JsonResponse({'status': False})


def builder(request):

    pokemon_list_raw = query.listPokedex()

    pokemon_list = []

    for elem in pokemon_list_raw['results']['bindings']:
        pokemon_list.append((elem['id']['value'], elem['name']['value'], elem['art']['value']))

    pokemon_paginator = Paginator(pokemon_list, 15)

    if request.is_ajax():

        page = request.GET.get('page', 1)

        pokemon_list = pokemon_paginator.page(int(page))

        pokemon_list_values = pokemon_list.object_list

        result = {'has_previous': pokemon_list.has_previous(),
                  'has_next': pokemon_list.has_next(),
                  'poke_li': pokemon_list_values}
        return JsonResponse(result)
    elif request.method == 'GET':

        tparams = {
            'pokemon_list': pokemon_paginator.page(1),
        }

        return render(request, 'team_builder.html', tparams)


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
