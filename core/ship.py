from models import Point

class Ship:
    def __init__(self, name: str, shape_coordinates: list[Point]):
        self.name: str = name
        self.shape_coordinates: list[Point] = shape_coordinates
        self.__actual_coordinates: list[Point] = None

    @property
    def actual_coordinates(self):
        return self.__actual_coordinates

    @actual_coordinates.setter
    def actual_coordinates(self, coordinates: list[Point]):
        self.__actual_coordinates: list[Point] = coordinates