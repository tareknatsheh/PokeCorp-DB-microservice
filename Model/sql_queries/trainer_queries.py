GET_BY_POKEMON_ID = """
    SELECT tr.id, tr.name, tr.town
    FROM (SELECT * FROM pokemons WHERE id = %s) p
    LEFT JOIN pokemon_trainers pktr ON p.id = pktr.pokemon_id
    LEFT JOIN trainers tr ON pktr.trainer_id = tr.id
"""

GET_ALL = "SELECT id, name, town FROM trainers"

GET_BY_ID = """
SELECT id, name, town FROM pokemon.trainers
WHERE id = %s
"""

ADD_POKEMON = """
INSERT INTO pokemon_trainers (trainer_id, pokemon_id)
VALUES (%s, %s)
"""

GET_TRAINER_POKEMON = """
SELECT pokemon_id, trainer_id FROM pokemon.pokemon_trainers
WHERE trainer_id = %s AND pokemon_id = %s
"""

EVOLVE_POKEMON = """
UPDATE pokemon.pokemon_trainers SET pokemon_id = %s
WHERE trainer_id = %s AND pokemon_id = %s;
"""