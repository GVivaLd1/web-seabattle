from enum import Enum
from pydantic import BaseModel

class CellState(Enum):
    EMPTY = 0
    SHIP = 1
    HIT = 2
    MISS = 3

class Point(BaseModel):
    x: int 
    y: int