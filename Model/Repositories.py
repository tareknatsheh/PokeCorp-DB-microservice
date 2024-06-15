from typing import Optional
from fastapi import HTTPException, status
from Model.Entities import Pokemon, Trainer
from Model.DB_Interface import DB_Interface

class Pokemon_Repo:
    def __init__(self, db: DB_Interface):
        self.db = db
    
    def add(self, new_pokemon: Pokemon) -> Pokemon:
        self.db.add_new_pokemon(new_pokemon)
        return new_pokemon
    
    def get_by_id(self, id: int) -> Pokemon:
        return self.db.get_pokemon_by_id(id)
    
    def get_by_trainer_id(self, trainer_id: int) -> list[dict]:
        return self.db.get_pokemons_by_trainer_id(trainer_id)
    
    def get_by_type(self, type: str) -> list[dict]:
        return self.db.get_pokemons_by_type(type)
    
    def get_by_type_and_trainer_id(self, type: str, trainer_id: int) -> list[dict]:
        return self.db.get_pokemons_by_type_and_trainer_id(type, trainer_id)
    

class Trainer_Repo:
    def __init__(self, db: DB_Interface):
        self.db = db

    def get_all(self) -> list[Trainer]:
        return self.db.get_all_trainers()
    
    def delete_a_pokemon(self, trainer_id: int, pokemon_id: int) -> Optional[int]:
        return self.db.delete_pokemon_of_trainer(trainer_id, pokemon_id)
    
    def get_by_pokemon_id(self, pokemon_id: int) -> list[Trainer]:
        return self.db.get_trainers_by_pokemon_id(pokemon_id)
    
    def is_have_pokemon(self, trainer_id: int, pokemon_id: int) -> bool:
        return self.db.is_trainer_has_pokemon(trainer_id, pokemon_id)
    
    def add_new_pokemon(self, trainer_id: int, pokemon_id: int) -> Pokemon:
        # 1. check if pokemon exist in our list, If not, return http exception
        pokemon_to_add = self.db.get_pokemon_by_id(pokemon_id)
        if not pokemon_to_add:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The Pokemon with ID {pokemon_id} could not be found.")
        # 2. check if trainer exist, if not, return http exception
        trainer_to_add_to = self.db.get_trainer_by_id(trainer_id)
        if not trainer_to_add_to:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The Trainer with ID {trainer_id} could not be found.")
        # 3. check if trainer already had this pokemon
        is_this_trainer_has_this_pokemon = self.db.is_trainer_has_pokemon(trainer_id, pokemon_id)
        # 4. if not, add it
        if is_this_trainer_has_this_pokemon:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"The Trainer {trainer_id} already has {pokemon_id}")
        result = self.db.add_new_pokemon_to_trainer(trainer_id, pokemon_to_add)
        if not result:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Adding pokemon with id {pokemon_id}, to trainer with id {trainer_id} has failed. Check the logs")
        return result
    
class Actions_Repo:
    def __init__(self, db: DB_Interface):
        self.db = db

    def evolve_pokemon_of_trainer(self, trainer_id: int, old_pokemon_id: int, new_pokemon_id: int) -> None:
        self.db.evolve_pokemon_of_trainer(trainer_id, old_pokemon_id, new_pokemon_id)