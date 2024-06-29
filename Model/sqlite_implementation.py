
import sqlite3
from decouple import config
from Model.Entities import Pokemon, Trainer
from typing import Any, Optional
from Model.DB_Interface import DB_Interface
from Model.utils.db_error_handler import handle_database_errors
import Model.sqlite_queries.pokemon_queries as pok_queries
import Model.sqlite_queries.trainer_queries as tr_queries

class SQLite_repo(DB_Interface):
    def __init__(self):
        self.db_connection = None
        self.cursor = None
    
    @handle_database_errors
    def get_all_pokemons(self) -> list[dict]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(pok_queries.GET_ALL)
        result = self.cursor.fetchall()
        result = [{"id": p[0], "name": p[1], "height": p[2], "weight": p[3]} for p in result]
        return result
    
    @handle_database_errors
    def get_pokemons_by_type(self, type: str) -> list[dict]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(pok_queries.GET_BY_TYPE, (type,))
        result = self.cursor.fetchall()
        result = [{"id": p[0], "name": p[1], "height": p[2], "weight": p[3]} for p in result]
        return result
    
    @handle_database_errors
    def get_pokemons_by_trainer_id(self, trainer_id: int) -> list[dict]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(pok_queries.GET_BY_TRAINER_ID, (trainer_id,))
        result = self.cursor.fetchall()
        result = [{"id": p[0], "name": p[1], "height": p[2], "weight": p[3]} for p in result]

        return result
    
    @handle_database_errors
    def get_pokemons_by_type_and_trainer_id(self, type, trainer_id) -> list[dict]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(pok_queries.GET_BY_TYPE_AND_TRAINER_ID, (trainer_id, type))
        result = self.cursor.fetchall()
        result = [{"id": p[0], "name": p[1], "height": p[2], "weight": p[3]} for p in result]

        return result

    @handle_database_errors
    def get_pokemon_by_id(self, id) -> Optional[Pokemon]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        self.cursor.execute(pok_queries.GET_BY_ID, (id,))
        result = self.cursor.fetchone()
        if not result:
            return None

        # Now the types of this pokemon:
        self.cursor.execute(pok_queries.GET_TYPES, (id,))
        all_types = self.cursor.fetchall()
        all_types = [t[1] for t in all_types]

        return Pokemon(id=result[0], name=result[1], height=result[2], weight=result[3], type=all_types)

    # done
    @handle_database_errors
    def add_new_pokemon(self, new_pok: Pokemon) -> Pokemon:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        if not self.db_connection:
            raise Exception("cursor not initialized")
        
        # First, add to pokemons table
        values = (new_pok.id, new_pok.name, new_pok.height, new_pok.weight)
        self.cursor.execute(pok_queries.ADD, values)
        self.db_connection.commit()

        # Then, add to types table:
        if not len(new_pok.type) == 0:
            for t in new_pok.type:
                values = (new_pok.id, t)
                self.cursor.execute(pok_queries.ADD_TYPES, values)
                self.db_connection.commit()

        return new_pok
    
    @handle_database_errors
    def get_trainers_by_pokemon_id(self, pokemon_id: int) -> list[Trainer]:
        print(f"looking for {pokemon_id}")
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.GET_BY_POKEMON_ID, (pokemon_id,))
        result = self.cursor.fetchall()

        print(result)

        if not result:
            return []
        return [Trainer(id=t[0], name=t[1], town=t[2]) for t in result]
    
    @handle_database_errors
    def get_all_trainers(self) -> list[Trainer]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.GET_ALL)
        result = self.cursor.fetchall()

        if not result:
            return []
        return [Trainer(id=t[0], name=t[1], town=t[2]) for t in result]
    
    @handle_database_errors
    def get_trainer_by_id(self, trainer_id: int) -> Optional[Trainer]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.GET_BY_ID, (trainer_id,))
        result = self.cursor.fetchone()
        if not result:
            return None
        return Trainer(id=result[0], name=result[1], town=result[2])
    
    @handle_database_errors
    def is_trainer_has_pokemon(self, trainer_id: int, pokemon_id) -> bool:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.GET_TRAINER_POKEMON, (trainer_id, pokemon_id))
        result = self.cursor.fetchone()
        if not result:
            return False
        return True
    
    @handle_database_errors
    def add_new_pokemon_to_trainer(self, trainer_id: int, pokemon: Pokemon) -> Pokemon:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        if not self.db_connection:
            raise Exception("cursor not initialized")
        
        values = (trainer_id, pokemon.id)
        self.cursor.execute(tr_queries.ADD_POKEMON, values)
        self.db_connection.commit()

        return pokemon

    @handle_database_errors
    def delete_pokemon_of_trainer(self, trainer_id, pokemon_id) -> int:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        if not self.db_connection:
            raise Exception("cursor not initialized")
        
        print(f"deleteing {trainer_id}/{pokemon_id}")

        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.DELETE_POKEMON_FROM_TRAINER, (trainer_id, pokemon_id))
        rows_affected = self.cursor.rowcount

        self.db_connection.commit()

        return rows_affected
    
    @handle_database_errors
    def evolve_pokemon_of_trainer(self, trainer_id: int, old_pokemon_id: int, new_pokemon_id: int) -> None:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        if not self.db_connection:
            raise Exception("cursor not initialized")
        
        values = (new_pokemon_id, trainer_id, old_pokemon_id)
        self.cursor.execute(tr_queries.EVOLVE_POKEMON, values)
        self.db_connection.commit()


    def _before(self):
        self.db_connection = sqlite3.connect(str(config("SQLITE_DB")) or "pokemons.db")
        self.cursor = self.db_connection.cursor()
    
    def _after(self):
        if self.cursor:
            self.cursor.close()
            print("db connection closed.")
        if self.db_connection:
            self.db_connection.close()


if __name__ == "__main__":
    # Sanity checking the DB repo
    mysql = SQLite_repo()
    a_pok = mysql.get_pokemon_by_id(34)
    print(a_pok)
        
    