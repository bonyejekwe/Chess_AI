# pieces.py:  defines classes for each chess piece type
# TODO implement a list of legal moves for each piece

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

    def get_color(self):
        return self._color  # if self._color == 1: # return "white" # else: # return "black"

    def get_position(self):
        return self._xpos, self._ypos

    def move(self, new_xpos, new_ypos):
        if (0 <= new_xpos <= 7) and (0 <= new_ypos <= 7):
            self._xpos = new_xpos
            self._ypos = new_ypos
        else:
            raise InvalidBoardPlacementError(new_xpos, new_ypos)

    def legal_moves(self):
        # return []
        pass


class Pawn(Piece):
    """Need to add additional (static?) methods for pawn movement implementation (ie: en passant, promotion).
        The movement according on color is based on: "white" = 1, "black" = -1 for simplicity"""

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos) == self._color:  # check condition validity
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        return "P"  # (actual representation)
        # return f"P: ({self._xpos}, {self._ypos})"  # test representation


class Knight(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if ((abs(new_xpos - self._xpos) == 1 and abs(new_ypos - self._ypos) == 2)
                or (abs(new_xpos - self._xpos) == 2 and abs(new_ypos - self._ypos) == 1)):  # L-shape movement
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        return "N"


class Bishop(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos):  # moves diagonally
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        return "B"


class Rook(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

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
                    moves.append((x, y))
        return moves

    def __str__(self):
        return "R"


class Queen(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if ((new_xpos - self._xpos) * (new_ypos - self._ypos) == 0 or
                (abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos))):  # move like bishop or move like rook
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        return "Q"


class King(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos <= 1) and abs(new_ypos - self._ypos <= 1):  # moves to adjacent square
            super().move(new_xpos, new_ypos)
        else:
            raise InvalidMoveError(new_xpos, new_ypos)

    def __str__(self):
        return "K"
