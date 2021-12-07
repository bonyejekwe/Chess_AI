# board.py: defines the board object

from pieces import *
from typing import Union
import collections
from profiler import Profiler


class Board:
    class WrongTeamError(Exception):
        pass

    class EmptySpaceError(Exception):
        pass

    class SpaceOccupiedError(Exception):
        pass

    class PieceInTheWayError(Exception):
        pass

    class NoKing(Exception):
        pass

    class InvalidPawnMove(Exception):
        pass

    class InvalidMoveError(Exception):
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
        self._game_over = False  # change when checkmate happens
        self._moves_since_capture = 0
        self._white_king_position = (4, 0)  # x, y indices of the white king
        self._black_king_position = (4, 7)  # x, y indices of the black king
        self._legal_moves = {}  # dictionary to temporarily store legal moves

        # dictionaries to store references to the piece objects (key=object, val = position tuple)
        self._white_pieces = {}
        self._black_pieces = {}

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
        empty = [[None for _ in range(8)] for _ in range(4)]
        self._board.append(white_back_row)
        self._board.append(white_pawns)
        for row in empty:
            self._board.append(row)
        self._board.append(black_pawns)
        self._board.append(black_back_row)
        self._turn = 1  # sets the turn to white
        self._moves_since_capture = 0
        self._move_count = 0
        self._game_over = False

        # initialize self._white_pieces and self._black_pieces
        for i in range(0, 8):
            for j in range(0, 8):
                if isinstance(self._board[i][j], Piece):
                    if self._board[i][j].get_color() == 1:
                        self._white_pieces[self._board[i][j]] = self._board[i][j].get_position()
                    elif self._board[i][j].get_color() == -1:
                        self._black_pieces[self._board[i][j]] = self._board[i][j].get_position()

    def get_pieces_left(self, color):
        if color == 1:
            return self._white_pieces
        elif color == -1:
            return self._black_pieces

    @Profiler.profile
    def update_pieces(self, piece, xpos, ypos, revert=False, delete=False, adding=False):
        """Updates the dictionaries every time a piece is moved"""
        if adding:
            if piece.get_color() == 1:
                self._white_pieces[piece] = piece.get_position()
            elif piece.get_color() == -1:
                self._black_pieces[piece] = piece.get_position()
            return 0

        if delete:
            if piece.get_color() == 1:
                self._white_pieces.pop(piece)
            elif piece.get_color() == -1:
                self._black_pieces.pop(piece)
            self._captured.append(piece)
            return 0

        if revert:
            piece.revert(xpos, ypos)
        else:
            piece.move(xpos, ypos)

        if piece.get_color() == 1:
            p = piece.get_position()
            self._white_pieces[piece] = p
        elif piece.get_color() == -1:
            p = piece.get_position()
            self._black_pieces[piece] = p

    def _start_test_game(self):
        """
        Starts a game for testing piece movement and game logic
        """
        b = [[None for _ in range(8)] for _ in range(8)]

        b[5][5] = King(5, 5, -1)
        b[7][7] = King(7, 7, 1)
        #
        b[6][6] = Queen(6, 6, -1)
        # b[1][3] = Pawn(3, 1, 1)
        # b[2][4] = Pawn(4, 2, -1)
        # b[3][5] = Pawn(5, 3, -1)
        # #b[3][3] = Rook(3, 3, -1)
        # b[7][5] = Pawn(5, 7, 1)
        # b[5][4] = Pawn(4, 5, 1)

        self._board = b
        self._turn = 1

    @Profiler.profile
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

        if pos2 not in self.legal_moves()[pos1]:
            raise Board.InvalidMoveError("The move {pos} is not in the board legal moves list".format(pos=position1))

        if self.is_position_empty(pos1):  # Trying to move a piece at a position that has no piece
            raise Board.EmptySpaceError("The space at {pos} is empty".format(pos=position1))
        piece1 = self.get_piece_from_position(pos1)

        if not self.validate_turn_color(piece1):  # Checks to see if it is that pieces turn
            raise Board.WrongTeamError("It is team {t1}'s turn, tried to move piece "
                                       "from team {t2}".format(t1=self._turn, t2=piece1.get_color()))

        # Checks to see if there are any pieces in between where a piece is and where it wants to go
        if self.is_piece_in_the_way(pos1, pos2):
            raise Board.PieceInTheWayError("There is(are) a piece(s) in between where you are and where you would"
                                           " like to move")

        piece2 = self.get_piece_from_position(pos2)

        if self.is_position_empty(pos2):  # if the place where the piece is trying to be moved to is empty it just moves
            if isinstance(piece1, Pawn) and pos2x != pos1x:  # sets pawn piece capture to false
                raise Board.InvalidPawnMove("Trying to move the pawn from {pos1} to {pos2}, which is diagonal but the"
                                            "pawn is not capturing".format(pos1=position1, pos2=position2))
            if not (isinstance(piece1, Pawn) and (pos2y == 7 or pos2y == 0)):  # regular move, makes sure a pawn doesn't have to be promoted
                self.update_pieces(piece1, pos2x, pos2y)  # piece1.move(pos2x, pos2y)
                self._board[pos2y][pos2x], self._board[pos1y][pos1x] = piece1, piece2
                self.update_move_count()
            else:  # Pawn promotion implementation
                # print("here")
                self.update_pieces(piece1, pos2x, pos2y)  # used to make sure pawn can't promote on wrong side
                self.update_pieces(piece1, pos2x, pos2y, delete=True)  # piece1.move(pos2x, pos2y)
                piece1 = Queen(pos2x, pos2y, piece1.get_color())
                self.update_pieces(piece1, pos2x, pos2y, adding=True)
                self._board[pos1y][pos1x], self._board[pos2y][pos2x] = None, piece1
                self.update_move_count()
            self._moves_since_capture += 1  # for checking endgame

        else:  # if the place is not empty
            # if the piece it is trying to move to is the other team it moves it and takes the other piece
            if not self.validate_turn_color(piece2):
                if isinstance(piece1, Pawn) and abs(pos2x - pos1x) != 1:
                    raise Board.InvalidPawnMove("Trying to move the pawn from {pos1} to {pos2} to capture, but did"
                                                "not move diagonal".format(pos1=position1, pos2=position2))
                self.update_pieces(piece1, pos2x, pos2y)  # piece1.move(pos2x, pos2y)  # moves individual piece object
                self._board[pos2y][pos2x], self._board[pos1y][pos1x] = piece1, None  # swaps positions on the board
                self.update_move_count()
                self.update_pieces(piece2, pos2x, pos2y, delete=True)
                self._captured.append(piece2)  # adds the captured piece to an array of captured pieces
                if isinstance(piece1, Pawn) and (pos2y == 7 or pos2y == 0):  # Pawn promotion after capture
                    self.update_pieces(piece1, pos2x, pos2y, delete=True)
                    piece1 = Queen(pos2x, pos2y, piece1.get_color())
                    self._board[pos2y][pos2x] = piece1
                    self.update_pieces(piece1, pos2x, pos2y, adding=True)

                self._moves_since_capture = 0  # for checking endgame
                return piece2  # returns the piece captured
            # otherwise catches the error when you try and capture a piece of the same team
            else:
                raise Board.WrongTeamError("Trying to capture piece at {pos} but it is the same team of {team}".format(
                    pos=position2, team=self._turn))
        return None

    @Profiler.profile
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
                lst_x = list(range(pos1x + step, pos2x, step))  # adds step so we don't consider current piece position

                # Determines the step for the range function to come up with values for diagonal
                if pos2y > pos1y:
                    step = 1
                else:
                    step = -1
                # Makes the list of the y values along the diagonal
                lst_y = list(range(pos1y + step, pos2y, step))  # adds step so we don't consider current piece position
                for x, y in zip(lst_x, lst_y):
                    in_the_way.append(self._board[y][x])
        # print(in_the_way)
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
        return in_the_way.count(None) != len(in_the_way)

    def switch_turn(self):
        """
        Switches the turn from white to black or black to white. Resets the dictionary for stored legal moves
        """
        self._turn *= -1
        self._legal_moves = {}

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

        if not (isinstance(piece, Piece) or piece is None):  # makes sure position actually holds a piece or is empty
            raise ValueError("Piece should not be of type {t} and value {v}".format(t=type(piece), v=piece))
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
                                 " a value of {value}".format(type1=type(self._board[position[1]][position[0]]),
                                                              value=self._board[position[1]][position[0]]))
        except IndexError:
            raise IndexError("The desired position is out of bounds of the board")

    def validate_turn_color(self, piece: Piece) -> bool:
        """
        Checks if the piece at the position is of the same color as the current color's turn
        :param piece: The piece you would like to check
        :return: True if the color and turn match up, false if not
        """
        return self._turn == piece.get_color()

    @staticmethod
    def letter_pos_to_num_pos(position: tuple) -> tuple:
        """
        Converts a position like (A,1) to (0,0)
        :param position: Position you would like convert
        :return: A tuple with two numbers as position
        """
        return ord(position[0]) - 65, position[1] - 1

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

    def get_current_move_count(self) -> int:
        return self._move_count

    def update_move_count(self, adding=True):
        if adding:
            self._move_count += 1
        else:
            self._move_count -= 1

    def __repr__(self):
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
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

    @Profiler.profile
    def is_in_check(self, c: int):
        """Returns where a specified team is in check or not
        :param c: the color corresponding to the specified team
        :return True if that team is in check and false otherwise"""
        # get the position of the corresponding king (from the dictionary of pieces left)
        # set consider to corresponding dictionary
        if c == 1:
            pos = self._white_pieces[[p for p in self._white_pieces.keys() if isinstance(p, King)][0]]
            consider = self._black_pieces
        else:
            pos = self._black_pieces[[p for p in self._black_pieces.keys() if isinstance(p, King)][0]]
            consider = self._white_pieces

        try:
            pos[0]
        except NameError:
            raise Board.NoKing(f'In is in check. {c} has no king.')

        checks = []

        for p in consider.keys():
            pos2 = p.get_position()
            if isinstance(p, Pawn):
                if (pos2[0] + 1 == pos[0] or pos2[0] - 1 == pos[0]) and pos2[1] + p.get_color() == pos[1]:  # checks if the king is diagonal to the pawn
                    return True
                    # checks.append(pos2)
            else:
                if p.can_move_to(pos[0], pos[1]) and (isinstance(p, Knight) or (not self.is_piece_in_the_way(pos2, pos))):
                    return True
                    # checks.append(pos2)
        return False
        # return len(checks) != 0

    @staticmethod
    def _is_white(piece: Piece) -> bool:
        """
        Checks if a certain piece is white or not
        :param piece: the piece which you would like to check if it is white
        :return: True if white, false otherwise
        """
        return isinstance(piece, Piece) and piece.get_color() == 1

    @Profiler.profile
    def legal_moves(self) -> dict:
        """
        Finds all possible legal moves of a certain color and returns them as a dictionary. Where the keys are
        a tuple as a position, and the values is a list of tuples each being a position. Only finds the legal moves of
        the pieces turn it is. If it is white's turn it only checks white's legal moves
        :return: Dictionary, key is tuple of position of a piece, value is a list of tuples as positions to where
        they key can move to.
        """
        if self._legal_moves != {}:
            return self._legal_moves

        possible_moves = collections.defaultdict(list)

        if self.get_current_turn() == 1:
            consider = self._white_pieces
        else:
            consider = self._black_pieces

        for piece1 in consider.keys():
            possible = piece1.legal_moves()
            piece1_position = consider[piece1]
            # print(piece1_position == consider[piece1])
            pos1x, pos1y = piece1_position

            for e in possible:
                if not self.is_piece_in_the_way(piece1_position, e):
                    piece2 = self._board[e[1]][e[0]]  # either None or Piece
                    if isinstance(piece2, Piece) and self.validate_turn_color(piece2):  # don't capture same team
                        continue
                    if (isinstance(piece1, Pawn) and ((isinstance(piece2, Piece) and (e[0]-pos1x == 0))
                                                      or (not isinstance(piece2, Piece) and abs(e[0]-pos1x) == 1))):
                        continue
                    if isinstance(piece2, King):  # don't add moves that capture the king
                        continue
                    self.update_pieces(piece1, e[0], e[1])  # piece1.move(e[0], e[1])  # temporarily make the move
                    if isinstance(piece2, Piece):  # temporarily delete piece from dict if necessary
                        pos2x, pos2y = piece2.get_position()
                        self.update_pieces(piece2, pos2x, pos2y, delete=True)
                    self._board[pos1y][pos1x], self._board[e[1]][e[0]] = None, self._board[pos1y][pos1x]
                    self.update_move_count()
                    if not self.is_in_check(self.get_current_turn()):
                        possible_moves[piece1_position].append(e)
                    self.update_pieces(piece1, pos1x, pos1y, revert=True)  # piece1.revert(pos1x, pos1y)  # unmake the temporary move
                    if isinstance(piece2, Piece):  # add back piece to dict if necessary
                        pos2x, pos2y = piece2.get_position()
                        self.update_pieces(piece2, pos2x, pos2y, adding=True)
                    self._board[pos1y][pos1x], self._board[e[1]][e[0]] = self._board[e[1]][e[0]], piece2
                    self.update_move_count(False)

        # if len(possible_moves) == 0:
        #    self._game_over = True

        self._legal_moves = possible_moves
        return possible_moves

    def checkmate(self, color) -> bool:
        """
        Determines if a team is in checkmate. Returns the color of the team in checkmate. If there is no one in
        checkmate, returns 0.
        :param color: 1 for white, -1 for black.
        :return: 1 for white in checkmate, -1 for black in checkmate, 0 for no one in checkmate
        """
        switch_team = False
        ret = False
        if self.get_current_turn() != color:
            self.switch_turn()
            switch_team = True
        if self.is_in_check(color) and len(self.legal_moves()) == 0:
            ret = True

        if switch_team:
            self.switch_turn()
        return ret

    def get_king_position(self, color: int) -> tuple:
        """
        Returns the position of the king as a tuple (x,y)
        :param color: 1 or -1 for white or black respectively
        :return: Tuple of the position of the king of specified color
        """
        if color == 1:
            piece = self.get_piece_from_position(self._white_king_position)
            if isinstance(piece, King) and piece.get_color() == color:
                return self._white_king_position
        elif color == -1:
            piece = self.get_piece_from_position(self._black_king_position)
            if isinstance(piece, King) and piece.get_color() == color:
                return self._black_king_position
        for i in range(8):  # y positions
            for j in range(8):  # x positions
                piece = self.get_piece_from_position((j, i))
                if isinstance(piece, King):
                    if color == 1 and piece.get_color() == 1:
                        self._white_king_position = (j, i)
                        return self._white_king_position
                    elif color == -1 and piece.get_color() == -1:
                        self._black_king_position = (j, i)
                        return self._black_king_position
        # print(self.__repr__())
        raise Board.NoKing("In get_king_positions. No king found of color: {c}".format(c=color))

    def is_game_over(self):
        if len(self.legal_moves()) == 0:
            print(f'game over')
            self._game_over = True
        elif self._moves_since_capture > 49:
            print(f'draw (50 move rule)')
            self._game_over = True
        return self._game_over

    def winner(self):
        if len(self.legal_moves()) == 0 and self.is_in_check(self._turn):
            print(f'checkmate')
            return self.get_current_turn() * -1
        elif len(self.legal_moves()) == 0:
            print(f'stalemate')
            return 2 * self.get_current_turn()
        else:
            return 0
