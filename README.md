# PokeCorp-DB-microservice

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

DONE!


