GET_ALL = "SELECT id, name, height, weight FROM pokemons"

GET_BY_TYPE = """
    SELECT pk.id, pk.name, pk.height, pk.weight 
    FROM (SELECT * FROM types WHERE type = ?) ty
    LEFT JOIN pokemons pk ON ty.pokemon_id = pk.id;
""" 
GET_BY_TRAINER_ID = """
    SELECT p.id, p.name, p.height, p.weight
    FROM (SELECT * FROM pokemon_trainers WHERE trainer_id = ?) pktr
    LEFT JOIN pokemons p ON p.id = pktr.pokemon_id;
"""
GET_BY_TYPE_AND_TRAINER_ID = """
    SELECT p.id, p.name, p.height, p.weight
    FROM (SELECT * FROM pokemon_trainers WHERE trainer_id = ?) pktr
    INNER JOIN pokemons p ON p.id = pktr.pokemon_id
    INNER JOIN (SELECT * FROM types WHERE type = ?) ty ON p.id = ty.pokemon_id;
"""
GET_BY_ID = "SELECT id, name, height, weight FROM pokemons WHERE id = ?"
GET_TYPES = "SELECT pokemon_id, type FROM types WHERE pokemon_id = ?"
ADD = "INSERT INTO pokemons (id, name, height, weight) VALUES (?, ?, ?, ?)"
ADD_TYPES = "INSERT INTO types (pokemon_id, type) VALUES (?, ?)"
