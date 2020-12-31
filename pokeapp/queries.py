# Queries.py
# A collection of SPARQL Queries for edc pokedex

from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

import json

endpoint = "http://localhost:7200"
repo_name = "edc-pokemon"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


def execute_select_query(query):
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    return res


def pokeGlobalInfo(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select ?p ?o
    where {{
        select ?s ?p ?o
        where{
             ?s pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """.
            ?s ?p ?o .
       }
   }
    
    }"""
    return execute_select_query(query)


def getAbilityDescription(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>

    select ?abilityname ?description where { 
        ?pokemon pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """.
        ?pokemon pok:ability ?ability .
        ?ability pok:name ?abilityname .
        ?ability pok:description ?description .
}   """
    return execute_select_query(query)


def getPokemonWeaknesses(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select DISTINCT ?weak 
    where {
    {
        select ?s ?p ?o
        where{
             ?s pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """.
             ?s ?p ?o .
       }
   }
    ?o pok:name ?type .
    ?o pok:isWeak ?weakT .
    ?weakT pok:name ?weak .    
    
} """
    return execute_select_query(query)


def getPokemonStrengths(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select DISTINCT ?strong
    where {
    {
        select ?s ?p ?o
        where{
             ?s pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """.
             ?s ?p ?o .
       }
   }
    ?o pok:name ?type .
    ?o pok:isSuperEffective ?strongT .
    ?strongT pok:name ?strong .   
    
} """
    return execute_select_query(query)


def getEvolutionLine(pokemon):  # to be finished, test with 3 evolutionary stage pokemon for now
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select ?name ?evolvesTo ?evoName ?pic ?number ?secondEvo ?secondEvoName ?secondPic ?secondNumber where {
     ?name pok:name """ + "\"" + str(pokemon) + "\"" + """.
     ?name pok:evolves-to ?evolvesTo .
     ?evolvesTo pok:name ?evoName .
     ?evolvesTo pok:art ?pic .
     ?evolvesTo pok:pokedex-entry ?number .
     ?evolvesTo pok:evolves-to ?secondEvo .
     ?secondEvo pok:name ?secondEvoName .
     ?secondEvo pok:art ?secondPic .
     ?secondEvo pok:pokedex-entry ?secondNumber .
    }   """
    return execute_select_query(query)


def getPokemonCategory(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>

    select ?categoryname where { 
        ?pokemon pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """.
        ?pokemon pok:category ?category .
        ?category pok:name ?categoryname .
    } """
    return execute_select_query(query)


def getPokemonType(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>

    select ?typename where { 
        ?pokemon pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """. 
        ?pokemon pok:type ?type .
        ?type pok:name ?typename .
    }"""
    return execute_select_query(query)


def getPreEvo(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select ?preEvoNumber where {
         ?preEvo pok:evolves-to ?pokemon .
         ?pokemon pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """.  
         ?preEvo pok:pokedex-entry ?preEvoNumber .    
    }"""
    return execute_select_query(query)


def getEvo(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select ?evoNumber where {
         ?pok pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """. 
         ?pok pok:evolves-to ?evolvesTo .
         ?evolvesTo pok:pokedex-entry ?evoNumber .  
    }"""
    return execute_select_query(query)


def getPokemonNumber(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    select ?poke where {
         ?pok pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """. 
         ?pok pok:pokedex-entry ?poke .  
    }
    """
    return execute_select_query(query)


def getEvolutionLine(pokemon_id):
    evoLine = []

    pre_evo_raw = getPreEvo(pokemon_id)
    pre_evo_list = list()
    for elem in pre_evo_raw['results']['bindings']:
        pre_evo_list.append(int(elem['preEvoNumber']['value']))
        evoLine.append(int(elem['preEvoNumber']['value']))

    evo_raw = getEvo(pokemon_id)
    evo_list = list()
    for elem in evo_raw['results']['bindings']:
        evo_list.append(int(elem['evoNumber']['value']))
        evoLine.append(int(elem['evoNumber']['value']))

    for poke in pre_evo_list:
        pre_pre_evo_raw = getPreEvo(poke)
        for elem in pre_pre_evo_raw['results']['bindings']:
            evoLine.append(int(elem['preEvoNumber']['value']))

    for poke in evo_list:
        second_evo_raw = getEvo(poke)
        for elem in second_evo_raw['results']['bindings']:
            evoLine.append(int(elem['evoNumber']['value']))

    actual_pokemon_raw = getPokemonNumber(pokemon_id)
    for elem in actual_pokemon_raw['results']['bindings']:
        evoLine.append(int(elem['poke']['value']))

    return sorted(evoLine)


def listPokedex():
    query = """
    prefix pok: <http://edcpokedex.org/pred/>

    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    select ?pokemonobj ?name where { 
        ?pokemonobj pok:pokedex-entry ?number FILTER (xsd:integer(?number)<=721) .
        ?pokemonobj pok:name ?name .
    } order by asc(xsd:integer(?number))     
    """
    return query


if __name__ == '__main__':
    print(getEvolutionLine(134))
