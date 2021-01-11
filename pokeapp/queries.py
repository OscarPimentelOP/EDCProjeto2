# Queries.py
# A collection of SPARQL Queries for edc pokedex

from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from SPARQLWrapper import SPARQLWrapper, JSON

import json

endpoint = "http://localhost:7200"
repo_name = "edc-pokemon"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

dbpedia_wrapper = SPARQLWrapper("http://live.dbpedia.org/sparql")


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


def getPokemonPicAndName(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    prefix poko: <http://edcpokedex.org/pokemon/>
    select ?poke_name ?poke_art  where {
         poko:""" + str(pokemon_id) + """ pok:art ?poke_art .  
         poko:""" + str(pokemon_id) + """ pok:name ?poke_name .
    }
    """
    return execute_select_query(query)


def getEvolutionLine(pokemon_id):
    evoLine = {
        "firstStage" : [],
        "secondStage": [],
        "thirdStage" : []
    }

    pre_evo_raw = getPreEvo(pokemon_id)
    pre_evo = [(int(elem['preEvoNumber']['value'])) for elem in pre_evo_raw['results']['bindings']]

    evo_raw = getEvo(pokemon_id)
    evo = [int(elem['evoNumber']['value']) for elem in evo_raw['results']['bindings']]

    pre_list = [pre_evo, []]
    for poke in pre_evo:
        pre_pre_evo_raw = getPreEvo(poke)
        pre_list[1] = ([(int(elem['preEvoNumber']['value'])) for elem in pre_pre_evo_raw['results']['bindings']])

    evo_list = [evo, []]
    for poke in evo:
       second_evo_raw = getEvo(poke)
       evo_list[1] = ([(int(elem['evoNumber']['value'])) for elem in second_evo_raw['results']['bindings']])

    actual_pokemon = [pokemon_id]

    if len(evo_list[1]) > 0:
        evoLine["firstStage"] = actual_pokemon
        evoLine["secondStage"] = evo_list[0]
        evoLine["thirdStage"] = evo_list[1]
    elif len(pre_list[1]) > 0:
        evoLine["firstStage"] = pre_list[1]
        evoLine["secondStage"] = pre_list[0]
        evoLine["thirdStage"] = actual_pokemon
    elif (len(pre_list[0]) == 0) and (len(evo_list[0]) >= 1):
        evoLine["firstStage"] = actual_pokemon
        evoLine["secondStage"] = evo_list[0]
        evoLine["thirdStage"] = []
    elif (len(pre_list[0]) >= 1) and (len(evo_list[0]) == 0):
        evoLine["firstStage"] = pre_list[0]
        evoLine["secondStage"] = actual_pokemon
        evoLine["thirdStage"] = []
    elif (len(pre_list[0]) == 0) and (len(evo_list[0]) == 0):
        evoLine["firstStage"] = actual_pokemon
        evoLine["secondStage"] = []
        evoLine["thirdStage"] = []
    else:
        evoLine["firstStage"] = pre_list[0]
        evoLine["secondStage"] = actual_pokemon
        evoLine["thirdStage"] = evo_list[0]

    return evoLine


def listPokedex():
    query = """
    prefix pok: <http://edcpokedex.org/pred/>

    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    select ?pokemonobj ?id ?name ?art where { 
        ?pokemonobj pok:pokedex-entry ?number FILTER (xsd:integer(?number)<=721) .
        ?pokemonobj pok:name ?name .
        ?pokemonobj pok:art ?art .
        ?pokemonobj pok:pokedex-entry ?id .
    } order by asc(xsd:integer(?number))     
    """
    return execute_select_query(query)


def listPokemonFromType(pokemon_type):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    select ?id ?name ?art where {
        ?pok pok:type ?type .
        ?type pok:name """ + "\"" + str(pokemon_type) + "\"" + """.  
        ?pok pok:pokedex-entry ?id .
        ?pok pok:name ?name .
        ?pok pok:art ?art .
    }    
    """
    return execute_select_query(query)


def searchListPokemonFromType(pokemon_type, word):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    select ?id ?name ?art where {
        ?pok pok:type ?type .
        ?type pok:name """ + "\"" + str(pokemon_type) + "\"" + """.  
        ?pok pok:pokedex-entry ?id .
        ?pok pok:name ?name .
        ?pok pok:art ?art .
        filter contains(?name,""" + "\"" + str(word) + "\"" + """)
    }order by asc(xsd:integer(?id)) 
    """
    return execute_select_query(query)


def search(word):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    select ?id ?name ?art where { 
        ?pokemonobj pok:pokedex-entry ?id FILTER (xsd:integer(?id)<=721) .
        ?pokemonobj pok:name ?name .
        ?pokemonobj pok:art ?art .
        filter contains(?name,""" + "\"" + str(word) + "\"" + """)
    } order by asc(xsd:integer(?id))     
    
    """
    return execute_select_query(query)

def getMatchups(type):
    query = """
    prefix pok2: <http://edcpokedex.org/type/>
    select ?type ?val where {           
        ?type """ + "" + str(type) + "" + """ ?val  .     
    } 
    """
    return execute_select_query(query)

def getChart(type):
    matchups = getMatchups(type)
    chart = ([(int(elem['val']['value'])) for elem in matchups['results']['bindings']])
    a = [x if x != 200 else "2x" for x in chart]
    a = [x if x != 100 else "1x" for x in a]
    a = [x if x != 50 else "1/2" for x in a]
    a = [x if x != 0 else "Immune" for x in a]

    return a

def getTypesPred(pokemon_id):
    query = """
    prefix pok: <http://edcpokedex.org/pred/>
    select ?typename where { 
        ?pokemon pok:pokedex-entry """ + "\"" + str(pokemon_id) + "\"" + """.   
        ?pokemon pok:type ?typename .
    }  
    """
    return execute_select_query(query)


def checkTeamExists(teamName):
    query = """
    prefix pred: <http://edcpokedex.org/pred/>
    prefix team: <http://edcpokedex.org/team/>

    ask {
        team:""" + str(teamName) + """  pred:name """ + "\"" + str(teamName) + "\"" + """.   
    }
    """
    return execute_select_query(query)

def insertTeam(teamName):
    query = """
    prefix pred: <http://edcpokedex.org/pred/>
    prefix team: <http://edcpokedex.org/team/>

    insert data {
        team:""" + str(teamName) + """  pred:name """ + "\"" + str(teamName) + "\"" + """. 
    }
    """
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query,
                                 repo_name=repo_name)
    return res

def deleteTeam(teamName):
    query = """
    prefix pred: <http://edcpokedex.org/pred/>
    prefix team: <http://edcpokedex.org/team/>

    delete data {
        team:""" + str(teamName) + """  pred:name """ + "\"" + str(teamName) + "\"" + """. 
    }
    """
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query,
                                 repo_name=repo_name)
    return res

def createNewTeam(teamName):
    teamExists = checkTeamExists(teamName)['boolean']

    if(teamExists):
        print("A team with that name already exists")
    else:
        insertTeam(teamName)

def insertPokeInTeam(pokemon_id, teamName):
    query = """
    prefix pred: <http://edcpokedex.org/pred/>
    prefix pok3: <http://edcpokedex.org/pokemon/> 
    prefix team: <http://edcpokedex.org/team/>

    insert data {
        team:""" + str(teamName) + """ pred:member pok3:""" + str(pokemon_id) + """ .
    }
    """
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query,
                                 repo_name=repo_name)
    return res

def deletePokemonFromTeam(pokemon_id, teamName):
    query = """
    prefix pred: <http://edcpokedex.org/pred/>
    prefix pok3: <http://edcpokedex.org/pokemon/> 
    prefix team: <http://edcpokedex.org/team/>
    
    delete data {
        team:""" + str(teamName) + """ pred:member pok3:""" + str(pokemon_id) + """ .
    }   
    """
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query,
                                 repo_name=repo_name)
    return res

def listTeamsAndPokemon(teamName):
    query = """    
    prefix pred: <http://edcpokedex.org/pred/>
    prefix pok3: <http://edcpokedex.org/pokemon/> 
    prefix team: <http://edcpokedex.org/team/>
    
    select ?id ?name ?art where{    
        team:""" + str(teamName) + """ pred:member ?pokemon .   
        ?pokemon pred:name ?name .   
        ?pokemon pred:pokedex-entry ?id .
        ?pokemon pred:art ?art . 
    }
    """
    return execute_select_query(query)

def dbpedia_query(query):
    dbpedia_wrapper.setQuery(query)
    dbpedia_wrapper.setReturnFormat(JSON)
    return dbpedia_wrapper.query().convert()


def get_dbpedia_pokemon_desc_and_pic():
    query = """
    prefix dbpedia: <http://dbpedia.org/resource/>
    prefix dbpedia-owl: <http://dbpedia.org/ontology/>

    select ?abstract ?thumbnail where { 
        dbpedia:Pokémon dbpedia-owl:abstract ?abstract ;
                           dbpedia-owl:thumbnail ?thumbnail .
        filter(langMatches(lang(?abstract),"en"))
    }
    """
    return dbpedia_query(query)


def get_dbpedia_pokemon_all_info():
    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?property ?hasValue ?isValueOf
    WHERE {
        { <http://dbpedia.org/resource/Pokémon> ?property ?hasValue }
        UNION
        { ?isValueOf ?property <http://dbpedia.org/resource/Pokémon> }
    }
    """
    return dbpedia_query(query)


def get_dbpedia_pokemon_game_list():
    query = """
    prefix dbpedia: <http://dbpedia.org/resource/>
    prefix dbpedia-owl: <http://dbpedia.org/ontology/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    
    select ?gamename, ?platform where { 
      ?game dbpedia-owl:series dbpedia:Pokémon_\(video_game_series\) ;
      foaf:name ?gamename ;
      dbpedia-owl:computingPlatform ?platform ;
      dbpedia-owl:releaseDate ?releaseDate .
    }
    """
    return dbpedia_query(query)


if __name__ == '__main__':
    # print(getEvolutionLine(493))
    # print(get_dbpedia_pokemon_desc_and_pic())
    # print(get_dbpedia_pokemon_game_list())
    # print(getPokemonPicAndName(1))
    # print(listPokemonFromType("Fire"))
    #print(searchListPokemonFromType("Electric", "chu"))
    # print(getChart("pok2:rock"))
    #print(createNewTeam("TestPython"))
    #print(checkTeamExists("TestPython"))
    #deleteTeam("TestPython")
    #insertPokeInTeam("18", "TestPython")
    print(listTeamsAndPokemon("TestPython"))

