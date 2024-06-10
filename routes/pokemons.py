from typing import Optional
from fastapi import APIRouter, HTTPException, status
from routes.utils.routes_error_handler import handle_route_errors
from Model.db import create_database
from Model.Entities import Pokemon

router = APIRouter()
db = create_database()

@router.get("/", status_code=status.HTTP_200_OK)
@handle_route_errors
def get_pokemon(type: Optional[str] = None, trainer_id: Optional[int] = None):
    """Get all pokemons, or filter by parameters
    Params:
        type: string
        trainer: string

    Returns:
        json: pokemon details
    """
    result = None
    if not type:
        if not trainer_id:
            # get all pokemons
            raise HTTPException(status_code=400, detail=f"There are too many pokemons, please specify a type and/or a trainer")
        else:
            # get by trainer
            result = db.pokemon.get_by_trainer_id(trainer_id)
    else:
        if not trainer_id:
            # get by type
            result = db.pokemon.get_by_type(type)
        else:
            # get by type and trainer id
            result = db.pokemon.get_by_type_and_trainer_id(type, trainer_id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Couldn't find any pokemon")

    print(result)
    return result

@router.get("/{id}", status_code=status.HTTP_200_OK)
@handle_route_errors
def get_pokemon_by_id(id: int):
    """Get pokemon by their unique id

    Returns:
        json: pokemon details
    """
    # pokemon = db.find_pokemon_by_id(id)
    pokemon = db.pokemon.get_by_id(id)

    if not pokemon:
        raise HTTPException(status_code=404, detail=f"Pokemon with id {id} could not be found")
    return pokemon

@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_route_errors
def add_new_pokemon(new_pokemon: Pokemon) -> Pokemon:
    """
    Pyload:
        id, name, height, weight, types (all of them)
    """
    return db.pokemon.add(new_pokemon)
