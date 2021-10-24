from pieces import *


class Board:
    def __init__(self):
        """
        board is 2d array of pieces and None objects. White is at the top, black is at the bottom so we can index the
        array easier. Because of this the board is upside down and flipped down the middle. Minor details.
        A1 is 0,0. H8 is 7,7
        Move count is number of moves
        """

        self._board = []
        self._move_count = 0
        self._turn = 0

    def start_game(self):
        """
        Starts game, fills in all pieces in the standard starting
        """
        white_back_row = [Rook(0,0, 0), Knight(1, 0, 0), Bishop(2, 0, 0), Queen(3, 0, 0), King(4, 0, 0), Bishop(5, 0, 0), Knight(6, 0, 0), Rook(7, 0, 0)]
        white_pawns = [Pawn(i,1,0) for i in range(8)]
        black_back_row = [Rook(0,7, 1), Knight(1,7, 1), Bishop(2,7, 1), Queen(3,7, 1), King(4,7, 1), Bishop(5,7, 1), Knight(6,7, 1), Rook(7,7, 1)]
        black_pawns = [Pawn(i, 6, 0) for i in range(8)]
        empty = [[None for i in range(8)] for i in range(4)]
        self._board.append(white_back_row)
        self._board.append(white_pawns)
        self._board.append(empty)
        self.board.append(black_pawns)
        self.board.append(black_back_row)





    def move_piece(self, position1: tuple,  position2: tuple):
        """
        Moves a piece from one position to another
        :param position1: A tuple containing a string and a number for x and y. Current Position
        :param position2: A tuple containing a string and a number for x and y. Desired Position
        :return: Nothing?
        """
        pos1 = self.letter_pos_to_num_pos(position1)
        pos2 = self.letter_pos_to_num_pos(position2)
        if not self.turn_and_color(pos1):
            raise ValueError("We really need an actual error not value error")




    def position_empty(self, position):
        """
        Checks if a desired position is empty
        :param position: Tuple of a position which you would like to check if a piece exists there
        :return: True if position is empty, false if not
        """

    def turn_and_color(self, position: tuple):
        """
        Checks if the piece at the position is of the same color as the current color's turn
        :param position: The position you would like to check
        :return: True if the color and turn match up, false if not
        """
        if self._turn == self._board[position[0]][position[1]].get_color():
            return True
        else:
            return False

    def letter_pos_to_num_pos(self, position: tuple):
        """
        Converts a position like A1 to (0,0)
        :param position: Position you would like convert
        :return: A tuple with two numbers as position
        """
        return (ord(position[1]) - 65, position[1])








    def __repr__(self):
        for i in self._board:
            for j in i:
                print(str(j) + " ", end="")
            print()
