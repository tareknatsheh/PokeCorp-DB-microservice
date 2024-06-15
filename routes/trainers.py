from fastapi import APIRouter, HTTPException, status
from Model.db import create_database
from routes.utils.routes_error_handler import handle_route_errors
from Model.Entities import Pokemon, Trainer

router = APIRouter()
db = create_database()

@router.get("/", status_code=status.HTTP_200_OK)
@handle_route_errors
def get_trainers_by_pokemon_id(pokemon_id: int):
    """Get trainers by pokemon they have
    Params:
        pokemon_id: int

    Returns:
        json: trainers
    """
    print("let's go")
    result: list[Trainer] = []
    if not pokemon_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a pokemon id")
    result = db.trainer.get_by_pokemon_id(pokemon_id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Couldn't find any trainer")

    return result

@router.delete("/{trainer_id}/{pokemon_id}")
@handle_route_errors
def delete_pokemon_of_trainer(trainer_id: int, pokemon_id: int):
    """Take a pokemon away from a trainer
    Path:
        trainer_id: int
        pokemon_id: int
    Returns:
        json: the deletion status
    """
    try:
        result = db.trainer.delete_a_pokemon(trainer_id, pokemon_id)
        return {
            "detail": f"Pokemon with id {pokemon_id} has been removed from trainer with id {trainer_id}",
            "affected_rows": result
        }

    except Exception as e:
        print(f"{e}")
        raise HTTPException(status_code=500, detail=f"Something went wrong, check the logs")


@router.put("/{trainer_id}/{pokemon_id}")
@handle_route_errors
def add_new_pokemon_to_trainer(trainer_id: int, pokemon_id: int):
    """add pokemon to a trainer: when a trainer catches a pokemon and train it the pokemon become his.
    params:
        pokemon_id
    """

    print(f"adding {pokemon_id} to {trainer_id} ")

    if not pokemon_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A Pokemon ID must be provided")
    
    result = db.trainer.add_new_pokemon(trainer_id, pokemon_id)
    return {
        "message": f"Pokemon with {pokemon_id} has been added to trainer with id {trainer_id}",
        "pokemon": {
            "id": result.id,
            "name": result.name,
            "height": result.height,
            "weight": result.weight,
            "type": result.type
        }
    }
    # return ""


