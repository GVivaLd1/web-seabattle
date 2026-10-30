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

                # Wrong ship placement (out of the board )
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

class TestBoardReceiveShot:

    @pytest.mark.parametrize(
                "target_point, target_initial_state, target_expected_state, expected_result",
                [
                    (
                        Point(x=3, y=3),
                        CellState.EMPTY,
                        CellState.MISS,
                        False
                    ),
                    (
                        Point(x=3, y=3),
                        CellState.SHIP,
                        CellState.HIT,
                        True
                    )
                ]    
    )
    def test_hit_changes_state(self, target_point: Point, 
                               target_initial_state: CellState, 
                               target_expected_state: CellState, 
                               expected_result: bool):
        board: Board = Board(10, 10)

        board.grid[target_point.x][target_point.y] = target_initial_state
        result: bool = board.receive_shot(target_point)

        assert board.grid[target_point.x][target_point.y] == target_expected_state
        assert result == expected_result

    def test_shoot_out_of_bound_raises_error(self):
        board: Board = Board(10, 10)
        target: Point = Point(x=12, y=-1)

        with pytest.raises(ValueError, match="The point is not within the game board"):
            board.receive_shot(target)

    @pytest.mark.parametrize(
            "target_state",
            [
                CellState.MISS,
                CellState.HIT
            ]
    )
    def test_shoot_already_targeted_cell_raises_error(self, target_state):
        board: Board = Board(10, 10)
        target: Point = Point(x=3, y=3)

        board.grid[target.x][target.y] = target_state

        with pytest.raises(ValueError, match="Cell already targeted"):
            board.receive_shot(target)
    
    def test_receive_shot_sinks_ship(self):
        board: Board = Board(10, 10)
        
        coords = [Point(x=0, y=0)]
        submarine = Ship("submarine", coords)
        board.add_ship(Point(x=5, y=5), submarine)
        
        assert board.check_is_all_ships_sunk() == False

        board.receive_shot(Point(x=5, y=5))

        assert board.check_is_all_ships_sunk() == True
