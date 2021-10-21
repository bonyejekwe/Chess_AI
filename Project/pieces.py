

class Piece:

    def __init__(self, xpos, ypos, color: int):
        self._xpos = xpos
        self._ypos = ypos
        self._color = color

    def move(self, new_xpos, new_ypos):
        if (0 <= new_xpos <= 7) and (0 <= new_ypos <= 7):
            self._xpos = new_xpos
            self._ypos = new_ypos
        else:
            print("Invalid board placement")


class Pawn(Piece):
    """Need to fix pawn movement implementation"""

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos) == 1:  # check condition validity
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def __str__(self):
        return f"P: ({self._xpos}, {self._ypos})"


class Knight(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if (abs(new_xpos - self._xpos) == 1 and abs(new_ypos - self._ypos) == 2) \
                or (abs(new_xpos - self._xpos) == 2 and abs(new_ypos - self._ypos) == 1):  # check condition validity
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def __str__(self):
        return f"N: ({self._xpos}, {self._ypos})"


class Bishop(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos):  # check condition validity for king
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def __str__(self):
        return f"B: ({self._xpos}, {self._ypos})"


class Rook(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if new_xpos == self._xpos or new_ypos == self._ypos:  # check condition for each specific piece
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def __str__(self):
        return f"R: ({self._xpos}, {self._ypos})"


class Queen(Piece):
    """Fix queen movement implementation"""

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if ((new_xpos == self._xpos or new_ypos == self._ypos) or (abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos))) \
                and not ((new_xpos == self._xpos or new_ypos == self._ypos) and (abs(new_xpos - self._xpos) == abs(new_ypos - self._ypos))):  # one of bishop and rook but not both
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def __str__(self):
        return f"Q: ({self._xpos}, {self._ypos})"


class King(Piece):

    def __init__(self, xpos, ypos, color):
        super().__init__(xpos, ypos, color)

    def move(self, new_xpos, new_ypos):
        if abs(new_xpos - self._xpos <= 1) and abs(new_ypos - self._ypos <= 1):  # check condition validity for king
            super().move(new_xpos, new_ypos)
        else:
            print("Invalid move")

    def __str__(self):
        return f"K: ({self._xpos}, {self._ypos})"

# Tests

r = Rook(0, 0, "black")
print(r)
r.move(3, 0)
print(r)
r.move(7, 3)
print(r)
r.move(3, 3)
print(r)
r.move(9, 3)
print(r)

k = King(0, 0, "white")
print(k)
k.move(1, 1)
print(k)
k.move(3, 3)
print(k)
k.move(2, 1)
print(k)
k.move(1, 1)
print(k)
k.move(0, 1)
print(k)
k.move(-1, 1)
print(k)
k.move(1, 1)
print(k)

b = Bishop(3, 0, "black")
print(b)
b.move(4, 1)
print(b)
b.move(5, 2)
print(b)
b.move(4, 1)
print(b)
b.move(3, 1)
print(b)
b.move(3, 2)
print(b)
b.move(4, 3)
print(b)
b.move(4, 1)
print(b)

q = Queen(0,0, "black")
print(q)
q.move(7, 0)
print(q)
q.move(7, 2)
print(q)
q.move(6, 1)
print(q)
q.move(4, 3)
print(q)
q.move(5, 1)
print(q)
q.move(5, 2)
print(q)
q.move(9, 0)


n = Knight(0, 0, "white")
print(n)
n.move(1, 2)
print(n)
n.move(1, 3)
print(n)
n.move(0, 4)
print(n)
n.move(1, 6)
print(n)
n.move(2, 6)
print(n)
n.move(2, 4)
print(n)
n.move(4, 5)
print(n)
n.move(1, 9)
print(n)
n.move(6, 6)
print(n)


print('\n')




l = [0] * 8

print(l)
print(l)
print(l)
print(l)
print(l)
print([0,0,0,1,0,0,0,0])
print(l)
print(l)