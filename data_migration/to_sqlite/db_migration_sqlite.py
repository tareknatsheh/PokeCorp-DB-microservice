def read_json_file(file_path: str) -> list[dict]:
    with open(file_path) as f:
        data = json.load(f)
        if not data:
            raise ValueError(f"There is no data in the provided file: {file_path}")
        return data


def db_init():  
    db_con = sqlite3.connect(str(config("SQLITE_DB")))
    return db_con

def migrate_pokemons_table(conn, data: list):
    cursor = conn.cursor()
    for pokemon in data:
        query = "INSERT INTO pokemons (id, name, height, weight) VALUES (?, ?, ?, ?)"
        values = (pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
        cursor.execute(query, values)
        conn.commit()


def migrate_trainers_table(conn, data: list):
    cursor = conn.cursor()
    all_trainers = {}
    for pokemon in data:
        pokemon_trainers: list[dict] = pokemon["ownedBy"]
        for trainer in pokemon_trainers:
            if not trainer["name"] in all_trainers:
                all_trainers[trainer["name"]] = trainer["town"]
                query = "INSERT INTO trainers (name, town) VALUES (?, ?)"
                values = (trainer["name"], trainer["town"])
                cursor.execute(query, values)
                conn.commit()

def migrate_types_table(conn, data: list):
    cursor = conn.cursor()

    for pokemon in data:
        for type in pokemon["type"]:
            query = "INSERT INTO types (pokemon_id, type) VALUES (?, ?)"
            values = (pokemon["id"], type)
            cursor.execute(query, values)
            conn.commit()

def migrate_pokemon_trainers_table(conn, data: list):
    cursor = conn.cursor()

    # get trainers table from SQL server
    query = "SELECT * FROM trainers"
    cursor.execute(query)
    result = cursor.fetchall()

    # get trainer id based on their name
    trainers_hash_table = {}
    for t in result:
        trainers_hash_table[t[1]] = t[0]

    # match it with .json data
    for pokemon in data:
        for trainer in pokemon["ownedBy"]:
            trainer_name = trainer["name"]
            trainer_id = trainers_hash_table[trainer_name]
            query = "INSERT INTO pokemon_trainers (pokemon_id, trainer_id) VALUES (?, ?)"
            values = (pokemon["id"], trainer_id)
            cursor.execute(query, values)
            conn.commit()


def init_db_from_sql():
    conn = sqlite3.connect(str(config("SQLITE_DB")))
    cursor = conn.cursor()
    with open("data_migration/to_sqlite/sql_scripts/sqlite_pokemon_db_schema.sql", 'r') as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    conn.commit()


def main():
    json_file_path = "data_migration/data seed/pokemons_data.json"

    connection = db_init()
    json_data = read_json_file(json_file_path)
    
    init_db_from_sql()
    migrate_pokemons_table(connection, json_data)
    migrate_trainers_table(connection, json_data)
    migrate_types_table(connection, json_data)
    migrate_pokemon_trainers_table(connection, json_data)

    connection.close()




if __name__ == "__main__":
    import sqlite3
    from decouple import config
    import json

    main()