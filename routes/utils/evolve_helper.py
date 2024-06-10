from typing import Any, Optional
from fastapi import HTTPException
import requests

def _get_name_and_evolution_chain_url_by_pokemon_id(pokemon_id) -> tuple:
    # get the pokemon details from pokeApi
    try:
        species_details = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}")
        species_details.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.HTTPError as http_err:
        if species_details.status_code == 404:
            print("Error 404: Resource not found.")
            raise HTTPException(status_code=404, detail=f"Pokemon with id {pokemon_id} could not be found")
        else:
            print(f"HTTP error occurred: {http_err}")
            raise HTTPException(status_code=500, detail=f"Something went wrong with pokeAPI")
    except Exception as err:
        print(f"An error occurred: {err}")
    else:
        species_details = species_details.json()
        if not "evolution_chain" in species_details:
            raise ValueError("The species details do not have evolution chain object")
        
        if not "url" in species_details["evolution_chain"]:
            raise ValueError("The species details have evolution chain but there is no 'url' KVP inside it!")
        
        evo_chain_url = species_details["evolution_chain"]["url"]

        if not "name" in species_details:
            raise ValueError("The species details do not have name KVP!")
        pokemon_name = species_details["name"]
        return pokemon_name, evo_chain_url
    
    return None, None

def _get_evolution_chain_object(evo_chain_url: str) -> dict:
    if not evo_chain_url:
        raise ValueError("You can't call _get_evolution_chain_object without having the evo chain url")
    evo_chain = requests.get(evo_chain_url).json()
    if not "chain" in evo_chain:
        raise ValueError("There is no 'chain' KVP in the evo chain!")
    return evo_chain["chain"]

def _find_next_evolution_name_and_id(pokemon_chain_obj: dict, pokemon_name) -> tuple[Optional[str], Optional[int]]:
    if not pokemon_name:
        raise ValueError("Can't evolve the pokemon without having its name!")
    if not pokemon_chain_obj:
        raise ValueError("No evolution chain object found!")
    if not "species" in pokemon_chain_obj:
        raise ValueError("The evolution chain object is missing the 'species' KVP")
    if not "name" in pokemon_chain_obj["species"]:
        raise ValueError("The 'species' KVP inside the evolution chain object is missing the 'name' KVP")
    
    print(f"checking: {pokemon_chain_obj["species"]["name"]}")

    # check the next evolution in line:
    if not "evolves_to" in pokemon_chain_obj:
        raise ValueError("The evolution chain object is missing the 'evolves_to' KVP")
    
    if pokemon_chain_obj["evolves_to"]:
        if not pokemon_chain_obj["species"]["name"] == pokemon_name:
            for chain_obj in pokemon_chain_obj["evolves_to"]:
                return _find_next_evolution_name_and_id(chain_obj, pokemon_name)
        else:
            print(f"Found him: {pokemon_chain_obj["species"]["name"]}, let's get the next evo")
            next_evo_name = pokemon_chain_obj["evolves_to"][0]["species"]["name"]
            evo_pokemon_name = next_evo_name
            print(f"It will be {next_evo_name}")
            next_evo_id = pokemon_chain_obj["evolves_to"][0]["species"]["url"].rstrip('/').split('/')[-1]
            evo_pokemon_id = int(next_evo_id)

            return evo_pokemon_name, evo_pokemon_id
    
    return (None, None)


def evolve(pokemon_id: int):
    pok_name, chain_url = _get_name_and_evolution_chain_url_by_pokemon_id(pokemon_id)
    evo_dict = _get_evolution_chain_object(chain_url)
    result = _find_next_evolution_name_and_id(evo_dict, pok_name)
    return result


if __name__ == "__main__":
    print("executing")
    print(evolve(11))

