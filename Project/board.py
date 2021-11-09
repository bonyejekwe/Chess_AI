from pieces import *
from typing import Union

class Board:

    class WrongTeamError(Exception):
        pass

    class EmptySpaceError(Exception):
        pass

    class SpaceOccupiedError(Exception):
        pass

    class PieceInTheWayError(Exception):
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
        self._turn = 1  # sets the turn to white
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
        self._turn = 1  # sets the turn to white

    def move_piece(self, position1: tuple, position2: tuple) -> Union[Piece, None]:
        """
        Moves a piece from one position to another
        :param position1: A tuple containing a string and a number for x and y. Current Position
        :param position2: A tuple containing a string and a number for x and y. Desired Position
        :return: The piece captured, or None if no piece is captured
        """

        pos1 = self.letter_pos_to_num_pos(position1)
        pos2 = self.letter_pos_to_num_pos(position2)
        pos1x, pos1y = pos1
        pos2x, pos2y = pos2

        if self.is_position_empty(pos1):  # Trying to move a piece at a position that has no piece
            raise Board.EmptySpaceError("The space at {pos} is empty".format(pos = position1))
        piece1 = self.get_piece_from_position(pos1)

        if not self.validate_turn_color(piece1):  # Checks to see if it is that pieces turn
            raise Board.WrongTeamError("It is team {t1}'s turn, tried to move piece "
                                       "from team {t2}".format(t1 = self._turn, t2 = piece1.get_color()))

        # Checks to see if there are any pieces in between where a piece is and where it wants to go
        if self.is_piece_in_the_way(pos1, pos2):
            raise Board.PieceInTheWayError("There is(are) a piece(s) in between where you are and where you would"
                                           " like to move")

        piece2 = self.get_piece_from_position(pos2)

        if self.is_position_empty(pos2):  # if the place where the piece is trying to be moved to is empty it just moves
            piece1.move(pos2x, pos2y)
            self._board[pos2y][pos2x], self._board[pos1y][pos1x] = piece1, piece2

        else:  # if the place is not empty
            if not self.validate_turn_color(piece2):  # if the piece it is trying to move to is the other team it moves it and takes the other piece
                piece1.move(pos2x, pos2y)  # moves the individual piece object
                self._board[pos2y][pos2x], self._board[pos1y][pos1x] = piece1, None  # swaps positions on the board
                self._captured.append(piece2)  # adds the captured piece to an array of captured pieces
                return piece2  # returns the piece captured
            else:  # catches the error when you try and capture a piece of the same team
                raise Board.WrongTeamError("Trying to capture piece at {pos} but it is the same team of {team}".format(
                    pos = position2, team = self._turn))
        return None

    def pieces_in_the_way(self, pos1: tuple, pos2: tuple) -> list:
        """
        Finds the pieces in between where a piece is and where it wants to go. It ignores knights as knights can jump
        over pieces
        :param pos1: The initial position of the piece
        :param pos2: Where the piece wants to go
        :return: A list of all the pieces or empty spaces in between where a piece is and where it wants to go
        """
        pos1x, pos1y = pos1
        pos2x, pos2y = pos2
        piece1 = self.get_piece_from_position(pos1)
        in_the_way = []
        # Checks to see if there are any pieces blocking each other
        # TODO Finish this
        if not isinstance(piece1, Knight):  # Knight can jump over pieces so it doesn't matter
            difx = pos2x - pos1x  # difference in y
            dify = pos2y - pos1y  # difference in x

            # Case where the piece moved only in the y direction
            if difx == 0:  # can assume dify != 0 as validate_turn_color will have thrown an error
                for i in range(min(pos1y, pos2y) + 1, max(pos1y, pos2y)):
                    in_the_way.append(self._board[i][pos2x])

            # Case where the piece only moved in the x direction
            elif dify == 0:  # can assume difx != 0 as validate_turn_color will have thrown an error
                in_the_way = self._board[pos2y][min(pos1x, pos2x) + 1:max(pos1x, pos2x)]

            # Case where the piece moved diagonally
            else:

                # Determines the step for the range function to come up with values for diagonal
                if pos2x > pos1x:
                    step = 1
                else:
                    step = -1
                # Makes the list of the x values along the diagonal
                lst_x = list(range(pos1x+step, pos2x, step))  # adds step so we don't consider where the piece currently is

                # Determines the step for the range function to come up with values for diagonal
                if pos2y > pos1y:
                    step = 1
                else:
                    step = -1
                # Makes the list of the y values along the diagonal
                lst_y = list(range(pos1y+step, pos2y, step))  # adds step so we don't consider where the piece currently is
                for x, y in zip(lst_x, lst_y):
                    in_the_way.append(self._board[y][x])
        #print(in_the_way)
        return in_the_way

        # noinspection PyUnreachableCode
        """
        The explanation of how the diagonal works: Say if you wanted to move Queen D1 to A3, which are indices 0,3 to 
        3,0, the piece would move: (y,x) [(0,3),(1,2),(2,1),(3,0)]. If instead you wanted to move Queen D1 to H5, 0,3 
        to 4,7, the piece would move: (y,x) [(0,3), (1,4), (2,5), (3,6), (4,7)]. If You wanted to move queen D8 to A5: 
        7,3 to 4,0: [(7,3), (6,2), (5,1), (4,0)] (y,x). If you wanted to move D8 to H4: 7,3 to 3,7: 
        [(7,3), (6,4), (5,5), (4,6), (3,7)]. Depending on which way the piece is moving diagonally changes which whether
        x or y is decreasing or increasing for the positions which need to be checked. So first it determines which way 
        the piece is moving in the x direction, whether it be to the left or to the right, if it is to the left, the 
        step is set to -1 so the range function decreases. It adds step to the initial value as it is just position 1 
        which we know is occupied. It does the exact same thing but for the y direction. It then iterates through all
        the pieces along the diagonal and adds each individual one to the array in_the_way
                
        """


    def is_piece_in_the_way(self, pos1: tuple, pos2: tuple) -> bool:
        """
        Checks if there are any pieces in the way between two different positions on the board
        :param pos1: The position as a tuple of indices of where the first piece is
        :param pos2: The position as a tuple of indices of where the first piece would like to go
        :return: True if there are pieces in the way, false if not
        """
        in_the_way = self.pieces_in_the_way(pos1, pos2)
        if in_the_way.count(None) != len(in_the_way):
            return True
        else:
            return False

    def switch_turn(self):
        """
        Switches the turn from white to black or black to white
        """
        self._turn *= -1

    def get_piece_from_position(self, position: tuple) -> Piece:
        """
        Returns a piece object or none from the board, raises error if the desired piece is neither a piece or empty
        :param position: A tuple of integers of the indices of the position desired
        :return: A piece object or None if no object is returned
        """
        if position[0] < 0 or position[1] < 0:
            raise IndexError("The desired position is out of bounds of the board")
        try:  # ensures the position is actually on the board
            piece = self._board[position[1]][position[0]]
        except IndexError:
            raise IndexError("The desired position is out of bounds of the board")

        if not (isinstance(piece, Piece) or piece is None):  # makes sure the position actually holds a piece or is empty
            raise ValueError("Piece should not be of type {t} and value {v}".format(t = type(piece),
                                                                                    v = piece))
        return piece

    def is_position_empty(self, position: tuple) -> bool:
        """
        Checks if a desired position is empty, returns true if Empty
        :param position: Tuple of indices a position which you would like to check if a piece exists there
        :return: True if position is empty, false if not
        """
        try:
            if self._board[position[1]][position[0]] is None:
                return True
            elif isinstance(self._board[position[1]][position[0]], Piece):
                return False
            else:
                raise ValueError("The board at this point is neither empty or a piece. It has a type of {type1} and has"
                                 " a value of {value}".format(type1 = type(self._board[position[1]][position[0]]),
                                                              value = self._board[position[1]][position[0]]))
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

    @staticmethod
    def letter_pos_to_num_pos(position: tuple) -> tuple:
        """
        Converts a position like (A,1) to (0,0)
        :param position: Position you would like convert
        :return: A tuple with two numbers as position
        """
        return (ord(position[0]) - 65, position[1]-1)

    def get_board(self) -> list:
        """
        :return: The board array
        """
        return self._board

    def get_captured(self) -> list:
        """
        :return: The list of captured items
        """
        return self._captured

    def get_current_turn(self) -> int:
        """
        1 is white, -1 is black
        :return: The integer representing who's turn it is
        """
        return self._turn

    def __repr__(self):
        alphabet = ["A","B", "C", "D", "E", "F", "G", "H"]
        num = 1
        string = " "
        for letter in alphabet:
            string += "{:>8}".format(letter)
        string += "\n\n"
        num = 1
        for i in self._board:
            string += str(num)
            num += 1
            for j in i:
                string += "{:>8}".format(str(j))
            string += "\n"
        return string
