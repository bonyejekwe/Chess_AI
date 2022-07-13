# board.py: defines the board object

from pieces import *
from typing import Union
import collections
from profiler import Profiler
from all_moves import all_positions


class NoKingError(Exception):

    def __init__(self, color):
        super().__init__(f"No king found of color {color}")


class InvalidMoveError(Exception):

    def __init__(self, pos1, pos2):
        super().__init__(f"The move {pos1} to {pos2} is not a legal move.")


class Board:

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
        self._game_over = False  # change when checkmate happens
        self._legal_moves = {}  # dictionary to temporarily store legal moves
        self._moves_list = []
        self._captured_pieces = []
        self._promoted_pawns = []
        self._moves_since_capture_list = []

        # store references to the piece objects {key=color, value={key=piece, val=pos}}
        self._pieces_left = collections.defaultdict(dict)

    def start_game(self):
        """Starts game, fills in all pieces in the standard starting"""
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
        self._move_count = 0
        self._game_over = False

        # initialize self._white_pieces and self._black_pieces
        for j, i in all_positions:  # iterate over all positions
            if isinstance(self._board[i][j], Piece):
                p = self._board[i][j]
                self._pieces_left[p.get_color()][p] = p.get_position()

    def get_pieces_left(self, color: int) -> dict:
        """
        Will get all of the pieces still on the board as well as their locations of a given color
        :param color: color you would like to get the pieces of
        :return: A dictionary of all the pieces for that color. key=piece object, value=position tuple
        """
        return self._pieces_left[color]

    @Profiler.profile
    def update_pieces(self, piece: Piece, xpos: int, ypos: int, revert=False, delete=False, adding=False):
        """
        Updates the dictionaries every time a piece is moved
        :param piece: The piece you would like to update
        :param xpos: The x position of the place you are moving the piece to
        :param ypos: The y position of the place you are moving the piece to
        :param revert: True if you would like to revert a move
        :param delete: True if you would like to delete a piece
        :param adding: True if you would like to add a piece to the colors piece dictionary
        """

        if adding:
            self._pieces_left[piece.get_color()][piece] = piece.get_position()
            return 0

        if delete:
            self._pieces_left[piece.get_color()].pop(piece)
            return 0

        if revert:
            piece.revert(xpos, ypos)
        else:
            piece.move(xpos, ypos)

        self._pieces_left[piece.get_color()][piece] = piece.get_position()

    def _start_test_game(self):
        """Starts a game for testing piece movement and game logic. (Testing purposes only!!!)"""
        b = [[None for _ in range(8)] for _ in range(8)]

        b[0][0] = King(0, 0, 1)
        b[5][6] = Pawn(6, 5, 1)
        b[7][0] = Bishop(0, 7, -1)
        b[7][7] = King(7, 7, -1)

        self._turn = 1  # sets the turn to white
        self._move_count = 0
        self._game_over = False
        self._board = b

        # initialize self._white_pieces and self._black_pieces
        for j, i in all_positions:  # iterate over all positions
            if isinstance(self._board[i][j], Piece):
                p = self._board[i][j]
                self._pieces_left[p.get_color()][p] = p.get_position()

    def get_moves_since_capture(self):
        """Get number of moves since the last capture"""
        i = 0
        for b in self._moves_since_capture_list[::-1]:
            if b:  # if b is True
                return i
            i += 1
        return i

    def _pawn_promotion(self, pawn: Pawn, pos2x: int, pos2y: int):
        """
        Promote a pawn by replacing it with a queen
        :return deleted pawn
        """
        self.update_pieces(pawn, pos2x, pos2y, delete=True)  # delete the pawn
        queen = Queen(pos2x, pos2y, pawn.get_color())
        self.update_pieces(queen, pos2x, pos2y, adding=True)  # add the queen
        return queen

    def _castle(self, king, pos2x):
        """Castle"""
        pos1x, pos2y = king.get_position()  # king has same ypos (pos1y == pos2y)
        if pos2x == 2:  # queen-side castle
            pos1x, pos2x = 0, 3  # old rook x and new rook x
        else:  # king-side castle (pos2x == 6)
            pos1x, pos2x = 7, 5  # old rook x and new rook x

        rook = self.get_piece_from_position((pos1x, pos2y))
        self._board[pos2y][pos2x], self._board[pos2y][pos1x] = rook, None
        self.update_pieces(rook, pos2x, pos2y)

    def _move_to_space(self, piece: Piece, pos2x: int, pos2y: int):
        """
        make move on board
        :return deleted pawn if it was promoted, None otherwise
        """
        pos1x, pos1y = piece.get_position()
        if isinstance(piece, Pawn) and (pos2y == 0 or pos2y == 7):
            self._promoted_pawns.append(piece)
            piece = self._pawn_promotion(piece, pos2x, pos2y)  # queen
        else:
            self._promoted_pawns.append(None)
            self.update_pieces(piece, pos2x, pos2y)

        self._board[pos2y][pos2x], self._board[pos1y][pos1x] = piece, None
        self.update_move_count()
        self._moves_since_capture_list.append(False)

        if isinstance(piece, King) and (abs(pos2x - pos1x) == 2):
            self._castle(piece, pos2x)

        self._captured_pieces.append(None)

    def _capture_piece(self, piece1, piece2):
        """capture piece2 with piece1"""
        pos1x, pos1y = piece1.get_position()
        pos2x, pos2y = piece2.get_position()
        if isinstance(piece1, Pawn) and (pos2y == 0 or pos2y == 7):  # Pawn promotion after capture
            self._promoted_pawns.append(piece1)
            piece1 = self._pawn_promotion(piece1, pos2x, pos2y)  # queen
        else:
            self._promoted_pawns.append(None)
            self.update_pieces(piece1, pos2x, pos2y)

        self._board[pos2y][pos2x], self._board[pos1y][pos1x] = piece1, None  # update positions on the board
        self.update_pieces(piece2, pos2x, pos2y, delete=True)  # delete captured piece
        self.update_move_count()
        self._moves_since_capture_list.append(True)
        self._captured_pieces.append(piece2)

    def _undo_promotion(self, pawn, queen, pos1):
        pos1x, pos1y = pos1
        pos2x, pos2y = queen.get_position()
        self.update_pieces(queen, pos2x, pos2y, delete=True)  # delete the queen
        self.update_pieces(pawn, pos1x, pos1y, adding=True)  # add the pawn
        return pawn

    def _undo_castle(self, king, pos2x):
        """Undo_castle, put the rook back"""
        pos1x, pos2y = king.get_position()  # king has same ypos (pos1y == pos2y)
        if pos2x == 2:  # was queen-side castle
            pos1x, pos2x = 0, 3  # old rook x and new rook x
        else:  # was king-side castle (pos2x == 6)
            pos1x, pos2x = 7, 5  # old rook x and new rook x

        rook = self.get_piece_from_position((pos2x, pos2y))
        self._board[pos2y][pos2x], self._board[pos2y][pos1x] = None, rook
        self.update_pieces(rook, pos1x, pos2y, revert=True)  # = (pos1x, pos1y)\

    def _undo_move_to_space(self, piece: Piece, pos1, promoted):
        """
        make move on board
        :return deleted pawn if it was promoted, None otherwise
        """
        pos1x, pos1y = pos1
        pos2x, pos2y = piece.get_position()
        if isinstance(promoted, Pawn):  # need to undo promote (piece is queen):
            piece = self._undo_promotion(promoted, piece, pos1)  # pawn
        else:
            self.update_pieces(piece, pos1x, pos1y, revert=True)

        self._board[pos2y][pos2x], self._board[pos1y][pos1x] = None, piece
        self.update_move_count(False)
        self._moves_since_capture_list.pop()

        if isinstance(piece, King) and (abs(pos2x - pos1x) == 2):
            self._undo_castle(piece, pos2x)

    def _undo_capture_piece(self, piece1, captured_piece, pos1, promoted):
        """undo capture piece2 with piece1"""
        pos1x, pos1y = pos1
        pos2x, pos2y = piece1.get_position()  # = captured_piece.get_position()  # piece1=queen

        if isinstance(promoted, Pawn):  # need to undo promote
            piece1 = self._undo_promotion(promoted, piece1, pos1)  # pawn
        else:
            self.update_pieces(piece1, pos1x, pos1y, revert=True)  # moves piece to new position

        self._board[pos2y][pos2x], self._board[pos1y][pos1x] = captured_piece, piece1  # update positions on the board
        self.update_pieces(captured_piece, pos2x, pos2y, adding=True)  # add captured piece
        self.update_move_count(False)
        self._moves_since_capture_list.pop()

    @Profiler.profile
    def move_piece(self, pos1: tuple, pos2: tuple, check=True) -> Union[Piece, None]:
        """
        Moves a piece from one position to another, checking the legality and correctness of the move
        :param pos1: A tuple containing int positions for x and y. Current Position
        :param pos2: A tuple containing int positions for x and y. Desired Position
        :param check: whether should check if in legal moves (can make False if only making move from legal moves)
        :return: The piece captured, or None if no piece is captured
        """
        piece1 = self.get_piece_from_position(pos1)  # can be piece or none
        piece2 = self.get_piece_from_position(pos2)  # can be piece or none

        # Note: legal moves shows all possible moves for the team whose turn it is
        if check:
            if (pos1 not in self.legal_moves().keys()) or (pos2 not in self.legal_moves()[pos1]):
                raise InvalidMoveError(pos1, pos2)

        self._moves_list.append((pos1, pos2))  # add move to list of moves
        if self.is_position_empty(pos2):  # if the place where the piece is trying to be moved to is empty
            self._move_to_space(piece1, pos2[0], pos2[1])  # make a move, promote pawn or castle if needed
        else:  # if the place moving to is not empty; capturing from other team
            self._capture_piece(piece1, piece2)  # return the captured piece
        return

    def undo_move(self):
        """Unmake the last move (pos1, pos2) from the board"""
        pos1, pos2 = self._moves_list.pop()  # get the last move
        pos1x, pos1y = pos1
        pos2x, pos2y = pos2
        piece1 = self.get_piece_from_position(pos2)

        captured_piece = self._captured_pieces.pop()
        promoted = self._promoted_pawns.pop()

        if captured_piece is None:  # a move to space:
            self._undo_move_to_space(piece1, pos1, promoted)
        else:  # a capture
            self._undo_capture_piece(piece1, captured_piece, pos1, promoted)

    # @Profiler.profile
    def is_piece_in_the_way(self, pos1x: int, pos1y: int, pos2x: int, pos2y: int) -> bool:
        """
        Checks if there are any pieces in the way between two different positions on the board
        :param pos1x: The x position of the first piece
        :param pos1y: The y position of the first piece
        :param pos2x: The x position of where the first piece would like to go
        :param pos2y: The y position of where the first piece would like to go
        :return: True if there are pieces in the way, false if not
        """
        piece1 = self.get_piece_from_position((pos1x, pos1y))

        if isinstance(piece1, Knight):  # Knight can jump over pieces so it doesn't matter
            return False

        # Checks to see if there are any pieces blocking each other
        dx = pos2x - pos1x  # difference in y
        dy = pos2y - pos1y  # difference in x

        # Case where the piece moved only in the y direction
        if dx == 0:  # can assume dy != 0 as validate_turn_color will have thrown an error
            for i in range(min(pos1y, pos2y) + 1, max(pos1y, pos2y)):
                if self._board[i][pos2x] is not None:
                    return True

        # Case where the piece only moved in the x direction
        elif dy == 0:  # can assume dx != 0 as validate_turn_color will have thrown an error
            for i in range(min(pos1x, pos2x) + 1, max(pos1x, pos2x)):
                if self._board[pos2y][i] is not None:
                    return True

        # Case where the piece moved diagonally (iterate over x from smallest to largest)
        else:
            minx, maxx = min(pos1x, pos2x), max(pos1x, pos2x)  # to iterate over x from smallest to largest
            if dy / dx > 0:  # positive if the slope is positive
                miny = min(pos1y, pos2y)
                for i in range(maxx - minx - 1):  # 0, 1, ... n, n is # in between
                    # if isinstance(self._board[miny + i + 1][minx + i + 1], Piece):
                    if self._board[miny + i + 1][minx + i + 1] is not None:
                        return True
            else:  # if the slope is negative
                maxy = max(pos1y, pos2y)
                for i in range(maxx - minx - 1):  # 0, 1, ... n, n is # in between
                    if self._board[maxy - i - 1][minx + i + 1] is not None:
                        return True
        return False

    def switch_turn(self):
        """Switches the turn from white to black or black to white. Resets the dictionary for stored legal moves"""
        self._turn *= -1
        self._legal_moves = {}

    def get_piece_from_position(self, position: tuple) -> Union[Piece, None]:
        """
        Returns a piece object or none from the board, raises error if the desired piece is neither a piece or empty
        :param position: A tuple of integers of the indices of the position desired
        :return: A piece object or None if no object is returned
        """
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

    def get_board(self) -> list:
        """
        :return: The board array
        """
        return self._board

    def get_captured(self) -> list:
        """:return: The list of captured items"""
        return self._captured_pieces

    def get_current_turn(self) -> int:
        """:return: The integer representing who's turn it is (1 is white, -1 is black)"""
        return self._turn

    def get_current_move_count(self) -> int:
        """:return: The current move count"""
        return self._move_count

    def update_move_count(self, adding=True):
        """
        Updates the current move count
        :param adding: adds if adding is true, if false it decreases move count
        """
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
        for i in range(7, -1, -1):
            string += str(i)
            for j in self._board[i]:  # each row
                string += "{:>8}".format(str(j))
            string += "\n"
        return string

    def is_attacked(self, pos1x: int, pos1y: int, c: int):
        """Return if a square is being attacked"""
        consider = self.get_pieces_left(-1 * c)  # set consider to corresponding dictionary (the other team's pieces)
        for p in consider.keys():
            pos2x, pos2y = consider[p]
            if isinstance(p, Pawn):
                # checks if the king is diagonal to the pawn
                if (pos2y + p.get_color() == pos1y) and (abs(pos2x - pos1x) == 1):
                    return True
            else:
                if p.can_move_to(pos1x, pos1y) and (not self.is_piece_in_the_way(pos2x, pos2y, pos1x, pos1y)):
                    return True

        return False

    @Profiler.profile
    def is_in_check(self, c: int):
        """Returns where a specified team is in check or not
        :param c: the color corresponding to the specified team
        :return True if that team is in check and false otherwise"""
        pos1x, pos1y = self.get_king_position(c)  # get corresponding king position (from the dictionary of pieces left)
        consider = self.get_pieces_left(-1 * c)  # set consider to corresponding dictionary (the other team's pieces)

        for p in consider.keys():
            pos2x, pos2y = consider[p]
            if isinstance(p, Pawn):
                # checks if the king is diagonal to the pawn
                if (pos2y + p.get_color() == pos1y) and (abs(pos2x - pos1x) == 1):
                    return True
            else:
                if p.can_move_to(pos1x, pos1y) and (not self.is_piece_in_the_way(pos2x, pos2y, pos1x, pos1y)):
                    return True

        return False

    @staticmethod
    def _is_white(piece: Piece) -> bool:
        """
        Checks if a certain piece is white or not
        :param piece: the piece which you would like to check if it is white
        :return: True if white, false otherwise
        """
        return isinstance(piece, Piece) and piece.get_color() == 1

    def castling_criteria(self, king, castle_move):
        """Return true if king can castle"""
        # if not isinstance(king, King):
        pos1x, pos1y = king.get_position()  # pos1x should be 4, pos2x should be 0 or 7 # need to check this
        if king.get_was_moved():  # check that king wasn't moved
            return False

        color = king.get_color()
        if self.is_in_check(color):
            return False

        # find the corresponding rook
        pos2x, pos2y = castle_move
        if pos2x == 2:  # queen-side castle
            rook_x = 0
            step = -1
        else:  # king-side castle (pos2x == 6)
            rook_x = 7
            step = 1
        # TODO need to check this

        r = self.get_piece_from_position((rook_x, pos2y))
        # check that corresponding rook wasn't moved
        if not (isinstance(r, Rook) and not r.get_was_moved()):
            return False

        # check the spaces are empty
        for x in range(4 + step, rook_x, step):  # all squares b/w except the current king square
            if not self.is_position_empty((x, pos1y)):
                return False

        # check that the two squares needed to be checked are both not being attacked
        if self.is_attacked((4 + step), pos1y, color) or self.is_attacked((4 + 2 * step), pos1y, color):
            return False

        return True

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
        consider = self.get_pieces_left(self.get_current_turn())

        for piece1, pos1 in consider.items():
            pos1x, pos1y = pos1  # = consider[piece1]
            for e1, e2 in piece1.legal_moves():
                if not self.is_piece_in_the_way(pos1x, pos1y, e1, e2):
                    piece2 = self._board[e2][e1]  # either None or Piece
                    if isinstance(piece2, Piece) and self.validate_turn_color(piece2):  # don't capture same team
                        continue
                    if (isinstance(piece1, Pawn) and ((isinstance(piece2, Piece) and (e1 == pos1x))
                                                      or (not isinstance(piece2, Piece) and abs(e1 - pos1x) == 1))):
                        continue
                    if isinstance(piece1, King) and (abs(e1 - pos1x) == 2) and (not self.castling_criteria(piece1, (e1, e2))):
                        continue  # continue if trying to castle but can't
                    if isinstance(piece2, King):  # don't add moves that capture the king
                        continue

                    self.update_pieces(piece1, e1, e2)  # temporarily make the move
                    if isinstance(piece2, Piece):  # temporarily delete piece from dict if necessary
                        pos2x, pos2y = piece2.get_position()
                        self.update_pieces(piece2, pos2x, pos2y, delete=True)

                    self._board[pos1y][pos1x], self._board[e2][e1] = None, self._board[pos1y][pos1x]
                    self.update_move_count()

                    if not self.is_in_check(self.get_current_turn()):
                        possible_moves[(pos1x, pos1y)].append((e1, e2))

                    self.update_pieces(piece1, pos1x, pos1y, revert=True)  # unmake the temporary move
                    if isinstance(piece2, Piece):  # add back piece to dict if necessary
                        pos2x, pos2y = piece2.get_position()
                        self.update_pieces(piece2, pos2x, pos2y, adding=True)
                    self._board[pos1y][pos1x], self._board[e2][e1] = self._board[e2][e1], piece2
                    self.update_move_count(False)

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
        # return [pos for piece, pos in self._pieces_left[color].items() if isinstance(piece, King)][0]
        consider = self._pieces_left[color].items()
        for piece, pos in consider:
            if isinstance(piece, King):
                return pos
        raise NoKingError(color)

    def is_game_over(self):
        """
        Determines whether or not the game is over based on if the team can no longer move, or if the draw states have
        been reached
        :return: True if the game is over, False if the game is not over
        """
        if len(self.legal_moves()) == 0:
            print('game over')
            self._game_over = True
        elif self.get_moves_since_capture() > 49:
            print('draw (50 move rule)')
            self._game_over = True
        elif self._move_count > 200:
            print('draw (200 move rule)')
            self._game_over = True
        return self._game_over

    def winner(self):
        """
        Determines which team won when the game ends
        :return: 1 white won, 2 for white put black in stalemate, negative numbers for black and 0 for a draw
        """
        if len(self.legal_moves()) == 0 and self.is_in_check(self._turn):
            print('checkmate')
            return self.get_current_turn() * -1
        elif len(self.legal_moves()) == 0:
            print('stalemate')
            return 2 * self.get_current_turn()
        else:
            return 0
