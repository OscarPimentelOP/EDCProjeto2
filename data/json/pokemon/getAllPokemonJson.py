import json
import requests

# Gets X pokemons from PokeAPI
# This is definitely not a good way to go about it, since it makes way to many requests
if __name__ == '__main__':
    for i in range(1, 722):
        pokemon = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(i))
        to_save = pokemon.json()
        poke_id = str(to_save['id'])
        with open(poke_id + '.json', 'w') as f:
            json.dump(to_save, f)
