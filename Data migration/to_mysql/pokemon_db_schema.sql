CREATE DATABASE IF NOT EXISTS pokemon;

USE pokemon;

DROP TABLE IF EXISTS pokemon_trainers;
DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS pokemons;
DROP TABLE IF EXISTS trainers;

CREATE TABLE pokemons(
	id INT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	height INT,
	weight INT
);

CREATE TABLE types(
    pokemon_id INT,
    type VARCHAR(50) NOT NULL,
    PRIMARY KEY (pokemon_id, type),
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE
);

CREATE TABLE trainers(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    town VARCHAR(50)
);

CREATE TABLE pokemon_trainers(
    pokemon_id INT,
    trainer_id INT,
    PRIMARY KEY (pokemon_id, trainer_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES trainers(id) ON DELETE CASCADE
);

