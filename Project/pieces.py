

class Piece:

    def __init__(self, xpos, ypos, color):
        self._xpos = xpos
        self._ypos = ypos
        self._color = color

    def move(self, xpos, ypos):
        self._xpos = xpos
        self._ypos = ypos


class Pawn(Piece):

    def __init__(self):
        pass

    def move(self, xpos, ypos):
        self._xpos = xpos
        self._ypos = ypos


class Knight(Piece):

    def __init__(self):
        pass

    def move(self, xpos, ypos):
        self._xpos = xpos
        self._ypos = ypos


class Bishop(Piece):

    def __init__(self):
        pass

    def move(self, xpos, ypos):
        self._xpos = xpos
        self._ypos = ypos


class Rook(Piece):

    def __init__(self):
        pass

    def move(self, xpos, ypos):
        self._xpos = xpos
        self._ypos = ypos


class Queen(Piece):

    def __init__(self):
        pass

    def move(self, xpos, ypos):
        self._xpos = xpos
        self._ypos = ypos


class King(Piece):

    def __init__(self):
        pass

    def move(self, xpos, ypos):
        self._xpos = xpos
        self._ypos = ypos
