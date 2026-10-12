from enum import Enum
from dataclasses import dataclass

class CellState(Enum):
    EMPTY = 0
    SHIP = 1
    HIT = 2
    MISS = 3

@dataclass
class Point:
    x: int 
    y: int