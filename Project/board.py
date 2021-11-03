from pieces import *


class Board:

    class WrongTeamError(Exception):
        pass

    class EmptySpaceError(Exception):
        pass

    class SpaceOccupiedError(Exception):
        pass

    def __init__(self):
        """
        board is 2d array of pieces and None objects. White is at the top, black is at the bottom so we can index the
        array easier. Because of this the board is upside down and flipped down the middle. Minor details.
        A1 is 0,0. H8 is 7,7
        Move count is number of moves
        """

        self._board = list()
        self._move_count = 0
        self._turn = 1
        self._captured = list()

    def start_game(self):
        """
        Starts game, fills in all pieces in the standard starting
        """
        white_back_row = [Rook(0, 0, 1), Knight(1, 0, 1), Bishop(2, 0, 1), Queen(3, 0, 1), King(4, 0, 1),
                          Bishop(5, 0, 1), Knight(6, 0, 1), Rook(7, 0, 1)]
        white_pawns = [Pawn(i, 1, 1) for i in range(8)]
        black_back_row = [Rook(0, 7, -1), Knight(1, 7, -1), Bishop(2, 7, -1), Queen(3, 7, -1), King(4, 7, -1),
                          Bishop(5, 7, -1), Knight(6, 7, -1), Rook(7, 7, -1)]
        black_pawns = [Pawn(i, 6, -1) for i in range(8)]
        empty = [[None for i in range(8)] for i in range(4)]
        self._board.append(white_back_row)
        self._board.append(white_pawns)
        for row in empty:
            self._board.append(row)
        self._board.append(black_pawns)
        self._board.append(black_back_row)
        self._turn = 1

    def move_piece(self, position1: tuple, position2: tuple):
        """
        Moves a piece from one position to another
        :param position1: A tuple containing a string and a number for x and y. Current Position
        :param position2: A tuple containing a string and a number for x and y. Desired Position
        :return: Nothing?
        """

        pos1 = self.letter_pos_to_num_pos(position1)
        pos2 = self.letter_pos_to_num_pos(position2)
        if self.is_position_empty(pos1):
            raise Board.EmptySpaceError("The space at {pos} is empty".format(pos=position1))
        piece1 = self.get_piece_from_position(pos1)

        if not self.validate_turn_color(piece1):  # checks to see if it is that pieces turn
            raise Board.WrongTeamError("It is team {t1}'s turn, tried to move piece "
                                       "from team {t2}".format(t1=self._turn, t2=piece1.get_color()))
        piece2 = self.get_piece_from_position(pos2)
        if self.is_position_empty(pos2):  # if the place where the piece is trying to be moved to is empty it just moves
            self._board[pos2[0]][pos2[1]] = piece1
            self._board[pos1[0]][pos1[0]] = piece2
        else:  # if the place is not empty
            if not self.validate_turn_color(piece2):  # if the piece it is trying to move to is the other team
                # TODO Need to figure out how we're deleting the piece from the board and how we want to return it
                #  would also like to try and add it to the captured pieces array
                self._board[pos2[0]][pos2[1]] = piece1
                self._board[pos1[0]][pos1[0]] = piece2
                #  self._captured.append(piece2)
            else:
                raise Board.WrongTeamError("Trying to capture piece at {pos} but it is the same team of {team}".format(
                    pos=position2, team=self._turn))

    def switch_turn(self):
        self._turn *= -1

    def get_piece_from_position(self, position: tuple) -> Piece:
        """
        Returns a piece object or none from the board, raises error if the desired piece is neither a piece or empty
        :param position: A tuple of integers of the indices of the position desired
        :return: A piece object or None if no object is returned
        """
        try:  # ensures the position is actually on the board
            piece = self._board[position[0]][position[1]]
        except IndexError:
            raise IndexError("The desired position is out of bounds of the board")

        if not (isinstance(piece, Piece) or piece is None):  # makes sure the position actually holds a piece or is empty
            raise ValueError("Piece should not be of type {t} and value {v}".format(t=type(piece),
                                                                                    v=piece))
        return piece

    def is_position_empty(self, position: tuple) -> bool:
        """
        Checks if a desired position is empty, returns true if Empty
        :param position: Tuple of indices a position which you would like to check if a piece exists there
        :return: True if position is empty, false if not
        """
        try:
            if self._board[position[0]][position[1]] is None:
                return True
            elif isinstance(self._board[position[0]][position[1]], Piece):
                return False
            else:
                raise ValueError("The board at this point is neither empty or a piece. It has a type of {type1} and has a "
                                 "value of {value}".format(type1=type(self._board[position[0]][position[1]]),
                                                           value=self._board[position[0]][position[1]]))
        except IndexError:
            raise IndexError("The desired position is out of bounds of the board")

    def validate_turn_color(self, piece: Piece) -> bool:
        """
        Checks if the piece at the position is of the same color as the current color's turn
        :param piece: The piece you would like to check
        :return: True if the color and turn match up, false if not
        """
        if self._turn == piece.get_color():
            return True
        else:
            return False

    def letter_pos_to_num_pos(self, position: tuple) -> tuple:
        """
        Converts a position like (A,1) to (0,0)
        :param position: Position you would like convert
        :return: A tuple with two numbers as position
        """
        return (ord(position[0]) - 65, position[1])

    def __repr__(self):
        string = ""
        for i in self._board:
            for j in i:
                string += str(j) + ","
            string += "\n"
        return string
