# board.py: defines the board object

from pieces import *
from typing import Union
import collections
from profiler import Profiler
from all_moves import all_positions, zobrist_table


class NoKingError(Exception):

    def __init__(self, color):
        super().__init__(f"No king found of color {color}")


class InvalidBoardMoveError(Exception):

    def __init__(self, pos1, pos2):
        super().__init__(f"The move {pos1} to {pos2} is not a legal move.")


class Board:

    def __init__(self):
        """A board is a 2D array of pieces and None objects. White pieces start at the beginning of the array. A1 is
        indexed at (0, 0) and H8 is indexed at (7, 7). Move count stores the number of moves"""
        self._board = []
        self._move_count = 0
        self._turn = 1  # sets the turn to white
        self._legal_moves = {}  # dictionary to temporarily store legal moves
        self._moves_list = []
        self._captured_pieces = []
        self._promoted_pawns = []
        self._moves_since_capture_list = []
        self._pieces_left = collections.defaultdict(dict)  # piece references {key=color, val={key=piece, val=pos}}
        self._zobrist_hash = 0
        self._zobrist_list = []

    def start_game(self):
        """Starts a standard chess game, initializes the board with pieces"""
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

        # iterate over all positions and initialize self._pieces_left with each piece
        for j, i in all_positions:
            if isinstance(self._board[i][j], Piece):
                p = self._board[i][j]
                self._pieces_left[p.get_color()][p] = p.get_position()

        self.zobrist_hash_init()  # initialize zobrist hash

    def _start_test_game(self):
        """Starts a game for testing piece movement and game logic. (Testing purposes only!!!)"""
        self._board = [[King(0, 0, 1), None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, Pawn(6, 5, 1), None],
                       [None, None, None, None, None, None, None, None],
                       [Bishop(0, 7, -1), None, None, None, None, None, None, King(7, 7, -1)]]

        self._turn = 1  # sets the turn to white
        self._move_count = 0

        # initialize self._white_pieces and self._black_pieces
        for j, i in all_positions:  # iterate over all positions
            if isinstance(self._board[i][j], Piece):
                p = self._board[i][j]
                self._pieces_left[p.get_color()][p] = p.get_position()

        self.zobrist_hash_init()  # initialize zobrist hash

    @Profiler.profile
    def get_zobrist_hash(self):
        return self._zobrist_hash

    def get_pieces_left(self, color: int) -> dict:
        """
        Will get all of the pieces still on the board as well as their locations of a given color
        :param color: team (1 or -1)
        :return: A dictionary of all the pieces for that team. {key=piece object, val=position tuple}
        """
        return self._pieces_left[color]

    def add_piece(self, piece: Piece):
        """Add a piece to self._pieces_left"""
        self._pieces_left[piece.get_color()][piece] = piece.get_position()

    def delete_piece(self, piece: Piece):
        """Delete a piece from self._pieces_left"""
        self._pieces_left[piece.get_color()].pop(piece)

    @Profiler.profile
    def update_pieces(self, piece: Piece, xpos: int, ypos: int, revert=False):
        """
        Updates self._pieces_left when time a piece is moved
        :param piece: The piece you would like to update
        :param xpos: The x position of the place you are moving the piece to
        :param ypos: The y position of the place you are moving the piece to
        :param revert: True if you would like to revert a move
        """
        if revert:
            piece.revert(xpos, ypos)
        else:
            piece.move(xpos, ypos)

        self._pieces_left[piece.get_color()][piece] = piece.get_position()

    def get_moves_since_capture(self):
        """Get number of moves since the last capture"""
        i = 0
        for b in self._moves_since_capture_list[::-1]:
            if b:  # if b is True
                return i
            i += 1
        return i

    def _pawn_promotion(self, pawn: Pawn, pos2x: int, pos2y: int):
        """Promote a pawn and replace it with a queen
        :return the queen"""
        self.delete_piece(pawn)  # delete the pawn
        queen = Queen(pos2x, pos2y, pawn.get_color())
        self.add_piece(queen)  # add the queen
        return queen

    def _castle(self, king, pos2x):
        """Complete a castle by moving and updating the corresponding rook"""
        pos1x, pos2y = king.get_position()  # king has same ypos (pos1y == pos2y)
        if pos2x == 2:  # queen-side castle
            pos1x, pos2x = 0, 3  # old rook x and new rook x
        else:  # king-side castle (pos2x == 6)
            pos1x, pos2x = 7, 5  # old rook x and new rook x

        rook = self.get_piece_from_position((pos1x, pos2y))
        self._zobrist_list.append((pos1x, pos2y, rook.get_idx()))
        self._board[pos2y][pos2x], self._board[pos2y][pos1x] = rook, None
        self.update_pieces(rook, pos2x, pos2y)
        self._zobrist_list.append((pos2x, pos2y, rook.get_idx()))

    def _move_to_space(self, piece: Piece, pos2x: int, pos2y: int):
        """
        make move on board
        :return deleted pawn if it was promoted, None otherwise
        """
        pos1x, pos1y = piece.get_position()
        self._zobrist_list.append((pos1x, pos1y, piece.get_idx()))
        if isinstance(piece, Pawn) and (pos2y == 0 or pos2y == 7):
            self._promoted_pawns.append(piece)
            piece = self._pawn_promotion(piece, pos2x, pos2y)  # queen
        else:
            self._promoted_pawns.append(None)
            self.update_pieces(piece, pos2x, pos2y)

        self._zobrist_list.append((pos2x, pos2y, piece.get_idx()))
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
        self._zobrist_list.append((pos1x, pos1y, piece1.get_idx()))
        if isinstance(piece1, Pawn) and (pos2y == 0 or pos2y == 7):  # Pawn promotion after capture
            self._promoted_pawns.append(piece1)
            piece1 = self._pawn_promotion(piece1, pos2x, pos2y)  # queen
        else:
            self._promoted_pawns.append(None)
            self.update_pieces(piece1, pos2x, pos2y)
        self._zobrist_list.append((pos2x, pos2y, piece1.get_idx()))
        self._zobrist_list.append((pos2x, pos2y, piece2.get_idx()))

        self._board[pos2y][pos2x], self._board[pos1y][pos1x] = piece1, None  # update positions on the board
        self.delete_piece(piece2)  # delete captured piece
        self.update_move_count()
        self._moves_since_capture_list.append(True)
        self._captured_pieces.append(piece2)

    def _undo_promotion(self, pawn, queen):
        """Undo a promotion; put the pawn back and delete the queen"""
        self.delete_piece(queen)  # delete the queen
        self.add_piece(pawn)  # add the pawn back
        return pawn

    def _undo_castle(self, king, pos2x):
        """Undo_castle, put the rook back"""
        pos1x, pos2y = king.get_position()  # king has same ypos (pos1y == pos2y)
        if pos2x == 2:  # was queen-side castle
            pos1x, pos2x = 0, 3  # old rook x and new rook x
        else:  # was king-side castle (pos2x == 6)
            pos1x, pos2x = 7, 5  # old rook x and new rook x

        rook = self.get_piece_from_position((pos2x, pos2y))
        self._zobrist_list.append((pos2x, pos2y, rook.get_idx()))
        self._board[pos2y][pos2x], self._board[pos2y][pos1x] = None, rook
        self.update_pieces(rook, pos1x, pos2y, revert=True)  # = (pos1x, pos1y)
        self._zobrist_list.append((pos1x, pos2y, rook.get_idx()))

    def _undo_move_to_space(self, piece: Piece, pos1, promoted):
        """make move on board
        :return deleted pawn if it was promoted, None otherwise"""
        pos1x, pos1y = pos1
        pos2x, pos2y = piece.get_position()
        self._zobrist_list.append((pos2x, pos2y, piece.get_idx()))
        if isinstance(promoted, Pawn):  # need to undo promote (piece is queen):
            piece = self._undo_promotion(promoted, piece)  # pawn
        else:
            self.update_pieces(piece, pos1x, pos1y, revert=True)
        self._zobrist_list.append((pos1x, pos1y, piece.get_idx()))
        self._board[pos2y][pos2x], self._board[pos1y][pos1x] = None, piece
        self.update_move_count(False)
        self._moves_since_capture_list.pop()

        if isinstance(piece, King) and (abs(pos2x - pos1x) == 2):
            self._undo_castle(piece, pos2x)

    def _undo_capture_piece(self, piece1, captured_piece, pos1, promoted):
        """undo capture piece2 with piece1"""
        pos1x, pos1y = pos1
        pos2x, pos2y = piece1.get_position()  # = captured_piece.get_position()  # piece1=queen
        self._zobrist_list.append((pos2x, pos2y, piece1.get_idx()))

        if isinstance(promoted, Pawn):  # need to undo promote
            piece1 = self._undo_promotion(promoted, piece1)  # pawn
        else:
            self.update_pieces(piece1, pos1x, pos1y, revert=True)  # moves piece to new position

        self._zobrist_list.append((pos1x, pos1y, piece1.get_idx()))
        self._zobrist_list.append((pos2x, pos2y, captured_piece.get_idx()))

        self._board[pos2y][pos2x], self._board[pos1y][pos1x] = captured_piece, piece1  # update positions on the board
        self.add_piece(captured_piece)  # add captured piece
        self.update_move_count(False)
        self._moves_since_capture_list.pop()

    @Profiler.profile
    def move_piece(self, pos1: tuple, pos2: tuple, check=True) -> None:
        """Moves a piece from one position to another, checking legality of move if specified
        :param pos1: A tuple containing int positions for x and y. Current Position
        :param pos2: A tuple containing int positions for x and y. Desired Position
        :param check: whether should check if in legal moves (can make False if only making move from legal moves)
        :return: The piece captured, or None if no piece is captured"""
        self._zobrist_list = []
        # Note: legal moves shows all possible moves for the team whose turn it is
        if check:
            if (pos1 not in self.legal_moves().keys()) or (pos2 not in self.legal_moves()[pos1]):
                raise InvalidBoardMoveError(pos1, pos2)

        self._moves_list.append((pos1, pos2))  # add move to list of moves

        piece1 = self.get_piece_from_position(pos1)  # can be piece or none
        if self.is_position_empty(pos2):  # if the place where the piece is trying to be moved to is empty
            self._move_to_space(piece1, pos2[0], pos2[1])  # make a move, promote pawn or castle if needed
        else:  # if the place moving to is not empty; capturing from other team
            piece2 = self.get_piece_from_position(pos2)  # can be piece or none
            self._capture_piece(piece1, piece2)  # return the captured piece
        self.switch_turn()
        lis = []  # TODO this
        self.update_zobrist_hash(self._zobrist_list)

    def undo_move(self):
        """Unmake the last move (pos1, pos2) from the board"""
        self._zobrist_list = []
        pos1, pos2 = self._moves_list.pop()  # get the last move
        piece1 = self.get_piece_from_position(pos2)

        captured_piece = self._captured_pieces.pop()
        promoted = self._promoted_pawns.pop()

        if captured_piece is None:  # a move to space:
            self._undo_move_to_space(piece1, pos1, promoted)
        else:  # a capture
            self._undo_capture_piece(piece1, captured_piece, pos1, promoted)
        self.switch_turn()
        lis = []  # TODO this
        self.update_zobrist_hash(self._zobrist_list)

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
        """Returns a piece object or none from the board, raises error if out of bounds error
        :param position: A tuple of integers of the indices of the position desired
        :return: A piece object or None if no object is returned
        """
        try:  # ensures the position is actually on the board
            return self._board[position[1]][position[0]]
        except IndexError:
            raise IndexError("The desired position is out of bounds of the board")

    def is_position_empty(self, position: tuple) -> bool:
        """Checks if a desired position is empty, returns true if Empty
        :param position: Tuple of indices a position which you would like to check if a piece exists there
        :return: True if position is empty, false if not"""
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
        """Checks if the piece at the position is of the same color as the current color's turn
        :param piece: The piece you would like to check
        :return: True if the color and turn match up, false if not"""
        return self._turn == piece.get_color()

    def get_board(self) -> list:
        """:return: The board array"""
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
        """Updates the current move count
        :param adding: adds if adding is true, if false it decreases move count"""
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

    # @Profiler.profile
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
        """Finds all possible legal moves for the team whose turn it is.
        :return: Dictionary, key is position tuple for a piece, value is list of tuples of positions it can move to."""
        if self._legal_moves != {}:
            return self._legal_moves

        possible_moves = collections.defaultdict(list)
        consider = self.get_pieces_left(self._turn)

        for piece1, pos1 in list(consider.items()):
            pos1x, pos1y = pos1  # = consider[piece1]
            for e1, e2 in piece1.legal_moves():
                if not self.is_piece_in_the_way(pos1x, pos1y, e1, e2):
                    piece2 = self._board[e2][e1]  # either None or Piece
                    if isinstance(piece2, Piece) and self.validate_turn_color(piece2):  # don't capture same team
                        continue
                    if (isinstance(piece1, Pawn) and ((isinstance(piece2, Piece) and (e1 == pos1x))
                                                      or (not isinstance(piece2, Piece) and abs(e1 - pos1x) == 1))):
                        continue
                    if isinstance(piece1, King) and (abs(e1 - pos1x) == 2) and (
                            not self.castling_criteria(piece1, (e1, e2))):
                        continue  # continue if trying to castle but can't
                    if isinstance(piece2, King):  # don't add moves that capture the king
                        continue

                    self.move_piece(pos1, (e1, e2), check=False)  # temporarily make the move

                    if not self.is_in_check(-1 * self._turn):  # add to list if legal
                        possible_moves[(pos1x, pos1y)].append((e1, e2))

                    self.undo_move()  # unmake the temporary move

        self._legal_moves = possible_moves
        return possible_moves

    @Profiler.profile
    def checkmate(self) -> bool:
        """
        Determines if the current team is in checkmate.
        :return: Returns true if the team is in checkmate, false otherwise.
        """
        return self.is_in_check(self._turn) and (len(self.legal_moves()) == 0)

    def get_king_position(self, color: int) -> tuple:
        """Returns the position of the king as a tuple (x,y)
        :param color: 1 or -1 for white or black respectively
        :return: Tuple of the position of the king of specified color"""
        consider = self._pieces_left[color].items()
        for piece, pos in consider:
            if isinstance(piece, King):
                return pos
        raise NoKingError(color)

    @Profiler.profile
    def is_game_over(self):
        """]Determines if game is over based on if the team can no longer move, or if game is a draw
        :return: True if the game is over, False if the game is not over"""
        if len(self.legal_moves()) == 0:
            print('game over')
            return True
        elif self.get_moves_since_capture() > 49:
            print('draw (50 move rule)')
            return True
        elif self._move_count > 200:
            print('draw (200 move rule)')
            return True
        return False

    def winner(self):
        """Determines which team won when the game ends
        :return: 3=white win, 1= white put black in stalemate, negative numbers for black, 0 for a draw (ie 200 move)"""
        if len(self.legal_moves()) == 0:
            if self.is_in_check(self._turn):
                print('checkmate')
                return self._turn * -3
            else:
                print('stalemate')
                return self._turn
        else:
            return 0

    @Profiler.profile
    def fen_hash(self):
        """Board hashing using modified Forsyth-Edwards Notation"""
        fen = ""
        for i in range(7, -1, -1):  # 7, 6, ..., 1, 0
            k = 0
            for j in self._board[i]:
                if isinstance(j, Piece):
                    if k > 0:
                        fen += str(k)
                    k = 0
                    fen += str(j)
                else:
                    k += 1

            if k > 0:
                fen += str(k)

        if self._turn == 1:
            fen += "w"
        else:
            fen += "b"

        white_king = self.get_piece_from_position((4, 0))
        if isinstance(white_king, King) and not white_king.get_was_moved():
            r = self.get_piece_from_position((7, 0))
            if isinstance(r, Rook) and not r.get_was_moved():
                fen += "K"
            r = self.get_piece_from_position((0, 0))
            if isinstance(r, Rook) and not r.get_was_moved():
                fen += "Q"

        black_king = self.get_piece_from_position((4, 7))
        if isinstance(black_king, King) and not black_king.get_was_moved():
            r = self.get_piece_from_position((7, 7))
            if isinstance(r, Rook) and not r.get_was_moved():
                fen += "k"
            r = self.get_piece_from_position((0, 7))
            if isinstance(r, Rook) and not r.get_was_moved():
                fen += "q"

        return fen

    def zobrist_hash_init(self):
        """Zobrist hashing"""
        self._zobrist_hash = 0
        for x, y in all_positions:
            p = self._board[y][x]
            if isinstance(p, Piece):
                self._zobrist_hash ^= zobrist_table[y][x][p.get_idx()]

    def update_zobrist_hash(self, lis):
        """lis = [(x_pos, y_pos, p_idx), ...]"""
        for pos in lis:
            x, y, idx = pos
            self._zobrist_hash ^= zobrist_table[y][x][idx]
