# PokeCorp-DB-microservice

You have two SQL database options:
- MySQL
- SQLite

You can switch to SQLite by setting the enviroment variable:
```USE_SQLITE=1```

You can also optionally set the db name using:
```SQLITE_DB=pokemons.db```

"pokemons.db" is the default value.

But if you decide to use MySQL, then you have to set the following env variables:
```
MYSQL_DB_PASSWORD="your_password"
MYSQL_HOST="localhost"
MYSQL_PORT=3307
```

Also, you have to create the databse tables, and do data migration. Here is how to create the tables using the provided .sql file:

#### Creating required SQL tables:

<details>
    <summary>From inside the docker container</summary>

    ### Step 1: Copy the `.sql` File to the Docker Container

    Assuming your MySQL Docker container is running and its name is `mysql_container`, you can use the `docker cp` command to copy the `.sql` file into the container:

    ```bash
    docker cp pokemon_db_schema.sql mysql_container:/pokemon_db_schema.
    ```

    ### Step 2: Access the MySQL Docker Container
    ```bash
    docker exec -it mysql_container /bin/bash
    ```

    ### Step 3: Execute SQL Commands Using MySQL Command-Line Client
    ```bash
    mysql -u root -p < /pokemon_db_schema.sql
    ```
</details>

<details>
<summary>Using the host SQL GUI</summary>

Alternativly, you can easily create the tables using a MySQL GUI application like MySQL workbench.

Just import the .sql file and run it.

</details>


### Data migration
<details>
<summary>SQLite</summary>
No need, the database pokemons.db is shipped with it.
</details>


<details>
<summary>MySQL</summary>
Check out the ```data_migration``` folder
</details>