# pieces.py:  defines classes for each chess piece type

# class InvalidMoveError(Exception):
# pass  # print("Invalid move")

# class InvalidBoardPlacementError(Exception):
# pass  # print("Invalid Board Placement")

class Piece:

    def __init__(self, xpos, ypos, color: int):
        self._xpos = xpos
        self._ypos = ypos
        self._color = color

    def get_color(self):
        return self._color
        # if self._color == 1:
        # return "white"
        # else:
        # return "black"

    def get_position(self):
        return self._xpos, self._ypos

    def move(self, new_xpos, new_ypos):
        if (0 <= new_xpos <= 7) and (0 <= new_ypos <= 7):
            self._xpos = new_xpos
            self._ypos = new_ypos
        else:
            print("Invalid Board Placement")  # raise InvalidBoardPlacementError(Exception)


class Pawn(Piece):
    """Need to fix pawn movement implementation. The movement according on color
        is based on: "white" = 1, "black" = -1 for simplicity"""

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos) == self._color:  # check condition validity
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")  # raise InvalidMoveError(Exception)

    def get_color(self):
        super().get_color()

    def get_position(self):
        super().get_position()

    def __str__(self):
        # return "P" (actual representation)
        return f"P: ({self._xpos}, {self._ypos})"  # test representation


class Knight(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if ((abs(new_xpos - self._xpos) == 1 and abs(new_ypos - self._ypos) == 2)
                or (abs(new_xpos - self._xpos) == 2 and abs(new_ypos - self._ypos) == 1)):  # L-shape movement
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def get_color(self):
        super().get_color()

    def get_position(self):
        super().get_position()

    def __str__(self):
        return f"N: ({self._xpos}, {self._ypos})"


class Bishop(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos):  # moves diagonally
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def get_color(self):
        super().get_color()

    def get_position(self):
        super().get_position()

    def __str__(self):
        return f"B: ({self._xpos}, {self._ypos})"


class Rook(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if (new_xpos - self._xpos) * (new_ypos - self._ypos) == 0:  # moves horizontally or vertically
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def get_color(self):
        super().get_color()

    def get_position(self):
        super().get_position()

    def __str__(self):
        return f"R: ({self._xpos}, {self._ypos})"


class Queen(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if ((new_xpos - self._xpos) * (new_ypos - self._ypos) == 0 or
                (abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos))):  # move like bishop or move like rook
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def get_color(self):
        super().get_color()

    def get_position(self):
        super().get_position()

    def __str__(self):
        return f"Q: ({self._xpos}, {self._ypos})"


class King(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos <= 1) and abs(new_ypos - self._ypos <= 1):  # moves to adjacent square
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def get_color(self):
        super().get_color()

    def get_position(self):
        super().get_position()

    def __str__(self):
        return f"K: ({self._xpos}, {self._ypos})"
