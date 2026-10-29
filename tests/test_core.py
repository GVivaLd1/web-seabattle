import pytest
from core.ship import Ship
from core.board import Board
from core.models import Point, CellState

class TestBoardAddShip:
     
    @pytest.mark.parametrize(
            "start_point, expected_result, expected_cells",
            [
                # Correct ship placement
                (
                    Point(x=2, y=2),
                    True,
                    (
                        (2, 2, CellState.SHIP), 
                        (2, 3, CellState.SHIP),
                        (2, 4, CellState.SHIP)
                    )
                ),

                # Wrong ship placement
                (
                    Point(x=2, y=8),
                    False,
                    (
                        (2, 8, CellState.EMPTY),
                        (2, 9, CellState.EMPTY)
                    )
                )
            ]
    )
    def test_on_clear_board(self, start_point: Point, expected_result: bool, expected_cells: tuple[tuple[int, int, CellState]]):
        board: Board = Board(width=10, height=10)
        
        coords: list[Point] = [Point(x=0, y=0), Point(x=0, y=1), Point(x=0, y=2)]
        cruiser: Ship = Ship("cruiser", coords)

        result: bool = board.add_ship(start_point, cruiser)

        assert result == expected_result

        for x, y, expected_state in expected_cells:
            assert board.grid[x][y] == expected_state

    @pytest.mark.parametrize(
            "start_point, expected_cells",
            [
                # Ship directly overlaps another
                (
                    Point(x=1, y=4),
                    (
                        (1, 4, CellState.EMPTY),
                        (2, 4, CellState.EMPTY),
                        (3, 4, CellState.SHIP)
                    )
                ),

                # Ship becomes a neighbor to another (forbidden by rules)
                (
                    Point(x=0, y=4),
                    (
                        (0, 4, CellState.EMPTY),
                        (1, 4, CellState.EMPTY),
                        (2, 4, CellState.EMPTY)
                    )
                )
            ]
    )
    def test_overlap(self, start_point: Point, expected_cells: tuple[tuple[int, int, CellState]]):
        board = Board(width=10, height=10)
        
        coords1 = [Point(x=0, y=0), Point(x=0, y=1), Point(x=0, y=2)]
        cruiser1 = Ship(name="cruiser1", shape_coordinates=coords1)
        board.add_ship(Point(x=3, y=3), cruiser1)
        
        coords2 = [Point(x=0, y=0), Point(x=1, y=0), Point(x=2, y=0)]
        cruiser2 = Ship(name="destroyer", shape_coordinates=coords2)

        result = board.add_ship(start_point, cruiser2)
        
        assert result == False
        
        for x, y, expected_state in expected_cells:
                assert board.grid[x][y] == expected_state