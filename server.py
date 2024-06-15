from fastapi import FastAPI
from routes import pokemons, trainers

app = FastAPI()

@app.get("/")
def main():
    return "DB server up and running"

app.include_router(pokemons.router, prefix="/api/pokemons", tags=["Pokemons routes"])
app.include_router(trainers.router, prefix="/api/trainers", tags=["Trainers routes"])