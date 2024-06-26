from typing import Optional
from Model.DB_Interface import DB_Interface
from Model.Repositories import Actions_Repo, Pokemon_Repo, Trainer_Repo
from decouple import config

# Check wether to use Sqlite or MySQL:
do_use_sqlit: int = int(config("USE_SQLITE")) or 0

db_repo: Optional[DB_Interface] = None
if do_use_sqlit:
    from Model.sqlite_implementation import SQLite_repo
    db_repo = SQLite_repo()
else:
    from Model.mysql_implementation import MySql_repo
    db_repo = MySql_repo()


class Database:
    def __init__(self):
        if not db_repo:
            raise ValueError("Make sure that you have USE_SQLITE in your env variables")
        self.my_db: DB_Interface = db_repo
        self.pokemon = Pokemon_Repo(self.my_db)
        self.trainer = Trainer_Repo(self.my_db)
        self.actions = Actions_Repo(self.my_db)
        pass

def create_database() -> Database:
    print("Creating a database instance (without connecting to it)")
    return Database()