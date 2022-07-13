
# pieces.py:  defines classes for each chess piece type

from profiler import Profiler
from all_moves import all_legal_moves_dict
from all_moves import all_positions


class InvalidMoveError(Exception):

    def __init__(self, xpos, ypos):
        super().__init__(f"Invalid move: Cannot move to ({xpos}, {ypos})")


class Piece:

    def __init__(self, xpos, ypos, color: int):
        self._original_xpos = xpos
        self._original_ypos = ypos
        self._xpos = xpos
        self._ypos = ypos
        self._color = color
        self._worth = 1
        self.num_moves = 0  # number of times piece was moved
        self._all_legal_moves = all_legal_moves_dict
        self._name = 'piece'
        # self._piece_legal_moves = 0#set()

    def get_color(self):
        """:return the color of the piece"""
        return self._color  # if self._color == 1: # return "white" # else: # return "black"

    def original_position(self):
        """:return the original position of the piece"""
        return self._original_xpos, self._original_ypos

    def get_position(self):
        """:return the current position of the piece"""
        return self._xpos, self._ypos

    def get_worth(self):
        """:return the worth of the piece"""
        return self._worth

    def get_was_moved(self):
        """
        Check if the piece was moved from the piece
        :return whether the piece was moved or not
        """
        return self.num_moves != 0

    def criteria(self, x, y):
        """Check whether a move to (x, y) fulfills the criteria for specific piece based on current position and piece
         itself. Return true if new x, y are both on the board and not the same as the old x, y
        :return bool for whether move fulfills criteria"""
        return (0 <= x <= 7) and (0 <= y <= 7) and not (x == self._xpos and y == self._ypos)

    def move(self, new_xpos, new_ypos):
        """Move the piece and decrement the was moved variable"""
        if self.criteria(new_xpos, new_ypos):
            self._xpos = new_xpos
            self._ypos = new_ypos
            self.num_moves += 1
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    @Profiler.profile
    def legal_moves(self):
        """Returns a list of legal moves for that piece based only on the restrictions for the piece type itself
        Inherited by all of the pieces to evaluate each piece's respective criteria"""
        return self._all_legal_moves[self._name][self._ypos][self._xpos]

    # @Profiler.profile
    def can_move_to(self, new_xpos, new_ypos):
        """Return true if piece can move to (new_xpos, new_ypos), false otherwise"""
        return (new_xpos, new_ypos) in self._all_legal_moves[self._name][self._ypos][self._xpos]  # self.legal_moves()

    def revert(self, last_xpos, last_ypos):
        """revert a piece back to its previous position (new_xpos, new_ypos). Decrement the was_moved variable"""
        self._xpos = last_xpos
        self._ypos = last_ypos
        self.num_moves -= 1


class Pawn(Piece):

    """The movement according on color is based on: "white" = 1, "black" = -1 for simplicity"""

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 1
        if color == 1:
            self._name = 'white_pawn'
        else:
            self._name = 'black_pawn'

    def pawn_first_move(self, new_xpos, new_ypos):
        """Returns true if pawn is trying to move 2 spaces for first move"""
        return (not self.get_was_moved()) and (new_ypos - self._ypos == 2 * self._color) and (new_xpos == self._xpos)

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills pawn movement criteria"""
        return (super().criteria(x, y) and (((y - self._ypos == self._color) and abs(x - self._xpos) <= 1) or
                                            self.pawn_first_move(x, y)))

    def __str__(self):
        if self.get_color() == 1:
            return "P"
        else:
            return "p"


class Knight(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 3
        self._name = 'knight'

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills knight l-shape movement criteria"""
        return (super().criteria(x, y) and (abs(x - self._xpos) == 1 and abs(y - self._ypos) == 2 or
                                            (abs(x - self._xpos) == 2 and abs(y - self._ypos) == 1)))

    def __str__(self):
        if self.get_color() == 1:
            return "N"
        else:
            return "n"


class Bishop(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 3
        self._name = 'bishop'

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills bishop diagonal movement criteria"""
        return super().criteria(x, y) and (abs(x - self._xpos) == abs(y - self._ypos))

    def __str__(self):
        if self.get_color() == 1:
            return "B"
        else:
            return "b"


class Rook(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 5
        self._name = 'rook'

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills rook movement criteria"""
        return super().criteria(x, y) and ((x - self._xpos) * (y - self._ypos) == 0)

    def __str__(self):
        if self.get_color() == 1:
            return "R"
        else:
            return "r"


class Queen(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 9
        self._name = 'queen'

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills queen's bishop or rook movement criteria"""
        return super().criteria(x, y) and \
            (x - self._xpos) * (y - self._ypos) == 0 or (abs(x - self._xpos) == abs(y - self._ypos))

    def __str__(self):
        if self.get_color() == 1:
            return "Q"
        else:
            return "q"


class King(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 90
        self._name = 'king'

    def king_castling(self, new_xpos, new_ypos):
        return (not self.get_was_moved()) and (abs(new_xpos - self._xpos) == 2) and (new_ypos == self._ypos)

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills king adjacent movement criteria"""
        return super().criteria(x, y) and (abs(y - self._ypos) <= 1) and ((abs(x - self._xpos) <= 1) or self.king_castling(x, y))

    def __str__(self):
        if self.get_color() == 1:
            return "K"
        else:
            return "k"

## Need to redo the criteria to redo the all-legal-moves-dict!!!

def get_moves_dict():
    moves_dict = {}
    for x, y in all_positions:  # [(0, 0), (1, 0), (2, 0), ...  (5, 7), (6, 7), (7, 7)]
        moves_dict[('white_pawn', (x, y))] = list(filter(lambda m: Pawn(x, y, 1).criteria(m[0], m[1]), all_positions))
        moves_dict[('black_pawn', (x, y))] = list(filter(lambda m: Pawn(x, y, -1).criteria(m[0], m[1]), all_positions))
        moves_dict[('knight', (x, y))] = list(filter(lambda m: Knight(x, y, 1).criteria(m[0], m[1]), all_positions))
        moves_dict[('bishop', (x, y))] = list(filter(lambda m: Bishop(x, y, 1).criteria(m[0], m[1]), all_positions))
        moves_dict[('rook', (x, y))] = list(filter(lambda m: Rook(x, y, 1).criteria(m[0], m[1]), all_positions))
        moves_dict[('queen', (x, y))] = list(filter(lambda m: Queen(x, y, 1).criteria(m[0], m[1]), all_positions))
        moves_dict[('king', (x, y))] = list(filter(lambda m: King(x, y, 1).criteria(m[0], m[1]), all_positions))

    return moves_dict

def reformat_current():
    d = all_legal_moves_dict
    new_dict = {}
    for piece_type, d1 in d.items():
        for ypos, d2 in d1.items():
            for xpos, lis in d2.items():
                new_dict[(piece_type, (xpos, ypos))] = lis
    return new_dict


#print(get_moves_dict())
#print("")
#print({k :v for k, v in get_moves_dict().items() if k[0] == "black_pawn"})

#print(reformat_current())
