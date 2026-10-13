from models import Point
from board import Board

class Game:
    def __init__(self, player1_board: Board, player2_board: Board): 
        self.__player1_board = player1_board
        self.__player2_board = player2_board
        self.__curr_player_turn = self.__player1_board

    # In addition to its primary function, checks whether any of the players have lost.
    def make_turn(self, player: Board, point: Point):
        if self.__curr_player_turn != player:
            return

        receiver = self.get_opposite_player()

        if receiver.receive_shot(point):
            pass
        else:
            self.__curr_player_turn = self.get_opposite_player()

        return receiver.check_is_all_ships_sunk()

    def get_opposite_player(self):
        return self.__player2_board if self.__player1_board == self.__curr_player_turn else self.__player1_board