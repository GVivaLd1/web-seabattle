from core.models import CellState, Point
from ship import Ship

class Board:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

        # Grid generation based on width & height
        self.grid: list[list[CellState]] = [[CellState.EMPTY for _ in range(self.width)] for _ in range(self.height)]

        # Ships located on the board
        self.__ships: list[Ship] = []

    # Adds ship to the grid if possible and returns boolean result
    def add_ship(self, start_point: Point, ship: Ship) -> bool:
        actual_ship_coordinates: list[Point] = []

        for point in ship.shape_coordinates:

            target_point = Point(
                x= start_point.x + point.x,
                y= start_point.y + point.y
            )

            if (
                self.check_borders(target_point)
                and self.grid[target_point.x][target_point.y] != CellState.SHIP
            ):
                actual_ship_coordinates.append((target_point))

            else: return False

        if self.check_ship_neighbors(actual_ship_coordinates): return False

        for point in actual_ship_coordinates:
            self.grid[point.x][point.y] = CellState.SHIP

        ship.actual_coordinates = actual_ship_coordinates
        self.__ships.append(ship)

        return True


    def receive_shot(self, point: Point) -> bool:
        if not self.check_borders(point):
            raise ValueError("The point is not within the game board.")
        
        match self.grid[point.x][point.y]:

            case CellState.EMPTY:
                self.grid[point.x][point.y] = CellState.MISS
                return False

            case CellState.SHIP:
                self.grid[point.x][point.y] = CellState.HIT

                sinked_ship = self.check_anyone_sunk()
                if sinked_ship != None:
                    self.__ships.remove(sinked_ship)

                return True

            case _:
                raise ValueError("Cell already targeted")

    # Calls on each shot
    def check_anyone_sunk(self) -> Ship | None:
        for ship in self.__ships:
            is_sunk = True

            for point in ship.actual_coordinates:
                if self.grid[point.x][point.y] != CellState.HIT:
                    is_sunk = False
                    break

            if is_sunk:
                return ship

        return None

    def check_is_all_ships_sunk(self) -> bool:
        if self.__ships == []:
            return True

        return False

    def check_ship_neighbors(self, coordinates: list[Point]) -> bool:

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for point in coordinates:
            for dx, dy in directions:
                neighbor_x = point.x + dx
                neighbor_y = point.y + dy
                
                if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:

                    if self.grid[neighbor_x][neighbor_y] == CellState.SHIP:
                        return True
                        
        return False

    def check_borders(self, point: Point) -> bool:
        if (
            point.x >= 0 
            and point.x < self.width
            and point.y >= 0 
            and point.y < self.height
        ):
            return True

        return False