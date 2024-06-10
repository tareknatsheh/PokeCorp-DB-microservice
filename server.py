from fastapi import FastAPI
from routes import pokemons

app = FastAPI()

@app.get("/")
def main():
    return "DB server up and running"

app.include_router(pokemons.router, prefix="/api/pokemons", tags=["Pokemons routes"])