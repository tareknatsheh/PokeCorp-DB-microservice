from pymongo.collection import Collection

def db_init() -> Collection:
    client: MongoClient = MongoClient("mongodb://localhost:5003/")
    cursor = client["PokeCorpDB"]
    collection = cursor["Pokemons"]
    return collection

def add_all(collection: Collection, pokemons: list[dict]):
    collection.insert_many(pokemons)

def generate_ids_for_trainers(data: list):
    all_trainers = {}
    id_counter = 1
    for pokemon in data:
        pokemon_trainers: list[dict] = pokemon["ownedBy"]
        for trainer in pokemon_trainers:
            if not trainer["name"] in all_trainers:
                all_trainers[trainer["name"]] = id_counter
                id_counter += 1
    
    return all_trainers


def update_db_trainers_ids(collection: Collection, trainers_ids: dict[str, int]):
    pokemons = collection.find({})

    # Update each Pokémon document
    for pokemon in pokemons:
        if 'ownedBy' in pokemon:
            for trainer in pokemon['ownedBy']:
                # Check if the trainer's name is in the dictionary and add the ID
                if trainer['name'] in trainers_ids:
                    trainer['id'] = trainers_ids[trainer['name']]
            
            # Update the document in the database
            collection.update_one(
                {'_id': pokemon['_id']},
                {'$set': {'ownedBy': pokemon['ownedBy']}}
            )

    print("Update complete.")

def read_json_file(file_path: str) -> list[dict]:
    with open(file_path) as f:
        data = json.load(f)
        if not data:
            raise ValueError(f"There is no data in the provided file: {file_path}")
        return data


def main():

    json_file_path = "D:/backend-bootcamp/Final project/PokeCorp/Data migration/data seed/pokemons_data.json"
    json_data = read_json_file(json_file_path)
    trainers_ids: dict = generate_ids_for_trainers(json_data)

    collection = db_init()
    add_all(collection, json_data)
    update_db_trainers_ids(collection, trainers_ids)


if __name__ == "__main__":
    from pymongo import MongoClient
    import json

    main()