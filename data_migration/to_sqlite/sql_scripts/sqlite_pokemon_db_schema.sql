-- Drop existing tables if they exist
DROP TABLE IF EXISTS pokemon_trainers;
DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS pokemons;
DROP TABLE IF EXISTS trainers;

-- Create the pokemons table
CREATE TABLE pokemons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    height INTEGER,
    weight INTEGER
);

-- Create the types table
CREATE TABLE types (
    pokemon_id INTEGER,
    type TEXT NOT NULL,
    PRIMARY KEY (pokemon_id, type),
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE
);

-- Create the trainers table
CREATE TABLE trainers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    town TEXT
);

-- Create the pokemon_trainers table
CREATE TABLE pokemon_trainers (
    pokemon_id INTEGER,
    trainer_id INTEGER,
    PRIMARY KEY (pokemon_id, trainer_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES trainers(id) ON DELETE CASCADE
);
