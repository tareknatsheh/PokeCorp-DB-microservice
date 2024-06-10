from Model.DB_Interface import DB_Interface
from Model.Repositories import Actions_Repo, Pokemon_Repo, Trainer_Repo
from Model.mysql_implementation import MySql_repo

class Database:
    def __init__(self):
        self.my_db: DB_Interface = MySql_repo()
        self.pokemon = Pokemon_Repo(self.my_db)
        self.trainer = Trainer_Repo(self.my_db)
        self.actions = Actions_Repo(self.my_db)
        pass

def create_database() -> Database:
    print("Creating a database instance (without connecting to it)")
    return Database()