# pieces.py:  defines classes for each chess piece type
# TODO: figure out how capturing is going to work with the pawn
# TODO: figure out how en-passant and castling (if time permits)

from profiler import Profiler

# all_positions: a SINGLE list (of len() = 64) of all board positions to filter piece legal moves
all_positions = [(i % 8, i // 8) for i in range(64)]  # [(0, 0), (1, 0), (2, 0), (3, 0), ...  (5, 7), (6, 7), (7, 7)]


class InvalidMoveError(Exception):

    def __init__(self, xpos, ypos):
        super().__init__(f"Invalid move: Cannot move to ({xpos}, {ypos})")


class InvalidBoardPlacementError(Exception):

    def __init__(self, xpos, ypos):
        super().__init__(f"Invalid Board Placement: Cannot move to ({xpos}, {ypos})")


class Piece:

    def __init__(self, xpos, ypos, color: int):
        self._original_xpos = xpos
        self._original_ypos = ypos
        self._xpos = xpos
        self._ypos = ypos
        self._color = color
        self._worth = 1
        self._was_moved = 1

    def get_color(self):
        return self._color  # if self._color == 1: # return "white" # else: # return "black"

    def original_position(self):
        return self._original_xpos, self._original_ypos

    def get_position(self):
        return self._xpos, self._ypos

    def get_worth(self):
        return self._worth

    def get_was_moved(self):
        if self._ypos == self.get_color():  # checks if the white pawn has moved from its starting position
            return False
        if self._ypos == -6 * self.get_color(): # checks if the black pawn has moved from its starting position
            # since black color is -1, and its starting y position if 6, if you multiple -1 by -6 it will = start y pos
            return False
        return True
        #return self._was_moved < 0

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if new x, y are both on the board and not the same as the old x, y"""
        return ((0 <= x <= 7) and (0 <= y <= 7)) and not (x == self._xpos and y == self._ypos)

    def move(self, new_xpos, new_ypos):
        if (0 <= new_xpos <= 7) and (0 <= new_ypos <= 7):
            self._xpos = new_xpos
            self._ypos = new_ypos
            self._was_moved -= 1
        else:
            raise InvalidBoardPlacementError(new_xpos, new_ypos)

    @Profiler.profile
    def legal_moves(self):
        """Returns a list of legal moves for that piece based only on the restrictions for the piece type itself
        Inherited by all of the pieces to evaluate each piece's respective criteria"""
        moves = all_positions
        return list(filter(lambda m: self.criteria(m[0], m[1]), moves))

    def can_move_to(self, new_xpos, new_ypos):
        """Return true if piece can move to (new_xpos, new_ypos), false otherwise"""
        return (new_xpos, new_ypos) in self.legal_moves()

    def revert(self, new_xpos, new_ypos):
        self._xpos = new_xpos
        self._ypos = new_ypos
        self._was_moved += 1


class Pawn(Piece):
    """The movement according on color is based on: "white" = 1, "black" = -1 for simplicity"""

    # TODO implement capturing correctly

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 1
        self._is_capturing = False

    def first_move(self, new_ypos):
        """Returns true if pawn is trying to move 2 spaces for first move"""
        return (not Pawn.get_was_moved(self)) and (new_ypos - self._ypos == 2 * self._color)

    def is_capturing(self):
        # TODO reimplement this correctly!!!!!!!
        return self._is_capturing

    def set_capturing(self, status):
        self._is_capturing = status  # True or False

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills pawn movement criteria"""
        # return (super().criteria(x, y) and ((y - self._ypos == self._color) or Pawn.first_move(self, y)) and
        #         (((abs(x - self._xpos) == 1) and self.is_capturing()) or (x == self._xpos and not self.is_capturing())))
        return (super().criteria(x, y) and (((y - self._ypos == self._color) and abs(x - self._xpos) <= 1) or
                                            (Pawn.first_move(self, y) and (x-self._xpos == 0))))

    def move(self, new_xpos, new_ypos):
        if self.criteria(new_xpos, new_ypos):
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        if self.get_color() == 1:
            return "P"
        else:
            return "P'"


class Knight(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 3

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills knight l-shape movement criteria"""
        return (super().criteria(x, y) and (abs(x - self._xpos) == 1 and abs(y - self._ypos) == 2 or
                                            (abs(x - self._xpos) == 2 and abs(y - self._ypos) == 1)))

    def move(self, new_xpos, new_ypos):
        if self.criteria(new_xpos, new_ypos):
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        if self.get_color() == 1:
            return "N"
        else:
            return "N'"


class Bishop(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 3

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills bishop diagonal movement criteria"""
        return super().criteria(x, y) and (abs(x - self._xpos) == abs(y - self._ypos))

    def move(self, new_xpos, new_ypos):
        if self.criteria(new_xpos, new_ypos):
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        if self.get_color() == 1:
            return "B"
        else:
            return "B'"


class Rook(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 5

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills rook movement criteria"""
        return super().criteria(x, y) and ((x - self._xpos) * (y - self._ypos) == 0)

    def move(self, new_xpos, new_ypos):
        if self.criteria(new_xpos, new_ypos):
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        if self.get_color() == 1:
            return "R"
        else:
            return "R'"


class Queen(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 9

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills queen's bishop or rook movement criteria"""
        return super().criteria(x, y) and \
            (x - self._xpos) * (y - self._ypos) == 0 or (abs(x - self._xpos) == abs(y - self._ypos))

    def move(self, new_xpos, new_ypos):
        if self.criteria(new_xpos, new_ypos):
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        if self.get_color() == 1:
            return "Q"
        else:
            return "Q'"


class King(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 90

    def criteria(self, x, y):
        """Return true if move to (x, y) fulfills criteria for specific piece based on current position and piece itself
        Here: true if piece criteria and fulfills king adjacent movement criteria"""
        return super().criteria(x, y) and (abs(x - self._xpos) <= 1) and (abs(y - self._ypos) <= 1)

    def move(self, new_xpos, new_ypos):
        if self.criteria(new_xpos, new_ypos):
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        if self.get_color() == 1:
            return "K"
        else:
            return "K'"
