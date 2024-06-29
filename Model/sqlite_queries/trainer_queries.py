GET_BY_POKEMON_ID = """
    SELECT tr.id, tr.name, tr.town
    FROM (SELECT * FROM pokemons WHERE id = ?) p
    LEFT JOIN pokemon_trainers pktr ON p.id = pktr.pokemon_id
    LEFT JOIN trainers tr ON pktr.trainer_id = tr.id
"""

GET_ALL = "SELECT id, name, town FROM trainers"

GET_BY_ID = """
SELECT id, name, town FROM trainers
WHERE id = ?
"""

ADD_POKEMON = """
INSERT INTO pokemon_trainers (trainer_id, pokemon_id)
VALUES (?, ?)
"""

GET_TRAINER_POKEMON = """
SELECT pokemon_id, trainer_id FROM pokemon_trainers
WHERE trainer_id = ? AND pokemon_id = ?
"""

DELETE_POKEMON_FROM_TRAINER="""
DELETE FROM pokemon_trainers
WHERE trainer_id = ? AND pokemon_id = ?
"""

EVOLVE_POKEMON = """
UPDATE pokemon_trainers SET pokemon_id = ?
WHERE trainer_id = ? AND pokemon_id = ?;
"""