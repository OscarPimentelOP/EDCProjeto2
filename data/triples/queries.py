def pokeGlobalInfo(pokemon):
    return """
    prefix pok: <http://edcpokedex.org/pred/
    
    select ?p ?o ?oname 
    where {{
        select ?s ?p ?o
        where{
             ?s pok:name """+"\""+str(pokemon)+"\""+""".
            ?s ?p ?o .
       }
   }
    
}"""

def getAbilityDescription(pokemon):
   return """
   prefix pok: <http://edcpokedex.org/pred/>
   select ?p ?o ?oname ?desc
    where {
    {
        select ?s ?p ?o
        where{
             ?s pok:name """+"\""+str(pokemon)+"\""+""".
             ?s ?p ?o .
       }
   }
    ?o pok:name ?oname .
    ?o pok:description ?desc
}  """

def getPokemonWeaknesses(pokemon):
    return """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select ?p ?o ?type ?weak 
    where {
    {
        select ?s ?p ?o
        where{
             ?s pok:name """+"\""+str(pokemon)+"\""+""".
             ?s ?p ?o .
       }
   }
    ?o pok:name ?type .
    ?o pok:isWeak ?weakT .
    ?weakT pok:name ?weak .    
    
} """

def getPokemonStrengths(pokemon):
    return """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select ?p ?o ?type ?strong
    where {
    {
        select ?s ?p ?o
        where{
             ?s pok:name """+"\""+str(pokemon)+"\""+""".
             ?s ?p ?o .
       }
   }
    ?o pok:name ?type .
    ?o pok:isSuperEffective ?strongT .
    ?strongT pok:name ?strong .   
    
} """

def getEvolutionLine(pokemon): #to be finished, test with 3 evolutionary stage pokemon for now
    return """
    prefix pok: <http://edcpokedex.org/pred/>
    
    select ?name ?evolvesTo ?evoName ?pic ?number ?secondEvo ?secondEvoName ?secondPic ?secondNumber where {
     ?name pok:name """+"\""+str(pokemon)+"\""+""".
     ?name pok:evolves-to ?evolvesTo .
     ?evolvesTo pok:name ?evoName .
     ?evolvesTo pok:art ?pic .
     ?evolvesTo pok:pokedex-entry ?number .
     ?evolvesTo pok:evolves-to ?secondEvo .
     ?secondEvo pok:name ?secondEvoName .
     ?secondEvo pok:art ?secondPic .
     ?secondEvo pok:pokedex-entry ?secondNumber .
    }   """

def listPokedex():
    return """
    prefix pok: <http://edcpokedex.org/pred/>

    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    select ?pokemonobj ?name where { 
        ?pokemonobj pok:pokedex-entry ?number FILTER (xsd:integer(?number)<=721) .
        ?pokemonobj pok:name ?name .
    } order by asc(xsd:integer(?number))     
    """