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
   select ?p ?o ?oname ?desc
    where {
    {
        select ?s ?p ?o
        where{
             ?s pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """.
             ?s ?p ?o .
       }
   }
    ?o pok:name ?oname .
    ?o pok:description ?desc
    }  """
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
    
    select ?p ?o ?type ?strong
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
