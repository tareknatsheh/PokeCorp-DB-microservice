from typing import Annotated
from pydantic import BaseModel, PositiveFloat, PositiveInt, StringConstraints

class Pokemon(BaseModel):
    id: PositiveInt
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    height: PositiveFloat
    weight: PositiveFloat
    type: list[str]

class Trainer(BaseModel):
    id: PositiveInt
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
    town: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
