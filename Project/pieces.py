
# pieces.py:  defines classes for each chess piece type
# TODO: figure out how capturing is going to work with the pawn
# TODO: figure out how en-passant and castling (if time permits)

class InvalidMoveError(Exception):

    def __init__(self, xpos, ypos):
        super().__init__(f"Invalid move: Cannot move to ({xpos}, {ypos})")


class InvalidBoardPlacementError(Exception):

    def __init__(self, xpos, ypos):
        super().__init__(f"Invalid Board Placement: Cannot move to ({xpos}, {ypos})")


class Piece:

    def __init__(self, xpos, ypos, color: int):
        self._xpos = xpos
        self._ypos = ypos
        self._color = color
        self._worth = 1
        self._was_moved = False

    def get_color(self):
        return self._color  # if self._color == 1: # return "white" # else: # return "black"

    def get_position(self):
        return self._xpos, self._ypos

    def get_worth(self):
        return self._worth

    def was_moved(self):
        return self._was_moved

    def move(self, new_xpos, new_ypos):
        if (0 <= new_xpos <= 7) and (0 <= new_ypos <= 7):
            self._xpos = new_xpos
            self._ypos = new_ypos
            self._was_moved = True
        else:
            raise InvalidBoardPlacementError(new_xpos, new_ypos)

    def legal_moves(self):
        moves = []
        for y in range(8):
            for x in range(8):
                if (0 <= x <= 7) and (0 <= y <= 7):
                    if not (x == self._xpos and y == self._ypos):
                        moves.append((x, y))
        return moves


class Pawn(Piece):
    """The movement according on color is based on: "white" = 1, "black" = -1 for simplicity"""
    # TODO implement capturing correctly

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 1
        self._is_capturing = False

    def first_move(self, new_ypos):
        """Returns true if pawn wants to move 2 spaces for first move"""
        return not Pawn.was_moved(self) and new_ypos - self._ypos == 2 * self._color

    def is_capturing(self):
        # TODO reimplement this correctly!!!!!!!
        return self._is_capturing

    def set_capturing(self, status):
        self._is_capturing = status  # True or False

    def move(self, new_xpos, new_ypos):
        if (new_ypos - self._ypos == self._color) or Pawn.first_move(self, new_ypos):
            if ((abs(new_xpos - self._xpos) <= 1) and self.is_capturing()) or new_xpos == self._xpos:
                super().move(new_xpos, new_ypos)  # first move up two

        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def legal_moves(self):
        moves = []
        for y in range(8):
            for x in range(8):
                if (y - self._ypos == self._color) or Pawn.first_move(self, y):
                    if (abs(x - self._xpos) <= 1 and self.is_capturing()) or x == self._xpos:
                        if not (x == self._xpos and y == self._ypos):
                            moves.append((x, y))
        return moves

    def __str__(self):
        if self.get_color() == 1:
            return "P"
        else:
            return "P'"


class Knight(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 3

    def move(self, new_xpos, new_ypos):
        if ((abs(new_xpos - self._xpos) == 1 and abs(new_ypos - self._ypos) == 2)
                or (abs(new_xpos - self._xpos) == 2 and abs(new_ypos - self._ypos) == 1)):  # L-shape movement
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def legal_moves(self):
        moves = []
        for y in range(8):
            for x in range(8):
                if (abs(x - self._xpos) == 1 and abs(y - self._ypos) == 2
                        or (abs(x - self._xpos) == 2 and abs(y - self._ypos) == 1)):  # L-shape movement
                    if not (x == self._xpos and y == self._ypos):
                        moves.append((x, y))
        return moves

    def __str__(self):
        if self.get_color() == 1:
            return "N"
        else:
            return "N'"


class Bishop(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 3

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos):  # moves diagonally
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def legal_moves(self):
        moves = []
        for y in range(8):
            for x in range(8):
                if abs(x - self._xpos) == abs(y - self._ypos):
                    if not (x == self._xpos and y == self._ypos):
                        moves.append((x, y))
        return moves

    def __str__(self):
        if self.get_color() == 1:
            return "B"
        else:
            return "B'"


class Rook(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 5

    def move(self, new_xpos, new_ypos):
        if (new_xpos - self._xpos) * (new_ypos - self._ypos) == 0:  # moves horizontally or vertically
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def legal_moves(self):
        moves = []
        for x in range(8):
            for y in range(8):
                if (x - self._xpos) * (y - self._ypos) == 0:
                    if not (x == self._xpos and y == self._ypos):
                        moves.append((x, y))
        return moves

    def __str__(self):
        if self.get_color() == 1:
            return "R"
        else:
            return "R'"


class Queen(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 9

    def move(self, new_xpos, new_ypos):
        if ((new_xpos - self._xpos) * (new_ypos - self._ypos) == 0 or
                (abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos))):  # move like bishop or move like rook
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def legal_moves(self):
        moves = []
        for y in range(8):
            for x in range(8):
                if (x - self._xpos) * (y - self._ypos) == 0 or (abs(x - self._xpos) == abs(y - self._ypos)):
                    if not (x == self._xpos and y == self._ypos):
                        moves.append((x, y))
        return moves

    def __str__(self):
        if self.get_color() == 1:
            return "Q"
        else:
            return "Q'"


class King(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)
        self._worth = 0

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos <= 1) and abs(new_ypos - self._ypos <= 1):  # moves to adjacent square
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def legal_moves(self):
        moves = []
        for x in range(self._xpos-1, self._xpos+2):
            for y in range(self._ypos - 1, self._ypos + 2):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if not (x == self._xpos and y == self._ypos):
                        moves.append((x, y))
        return moves

    def __str__(self):
        if self.get_color() == 1:
            return "K"
        else:
            return "K'"
