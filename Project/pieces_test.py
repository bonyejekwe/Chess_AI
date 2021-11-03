
from pieces import *


# Tests
print('Piece Tests:')
p1 = Piece(0, 0, 1)
print(f"Color: {p1.get_color()}")
print(f"Position: {p1.get_position()}")

print('\nRook Tests:')
r = Rook(0, 0, -1)  # 0 = "black"
print(f"Color: {r.get_color()}")
print(f"{r}: {r.get_position()}")
r.move(3, 0)
print(f"{r}: {r.get_position()}")
r.move(7, 3)  # should be invalid move
print(f"{r}: {r.get_position()}")
r.move(3, 3)
print(f"{r}: {r.get_position()}")
r.move(9, 3)  # should be invalid board placement
print(f"{r}: {r.get_position()}")

print('\nKing Tests:')
k = King(0, 0, 1)  # 1 = "white"
print(f"Color: {k.get_color()}")
print(f"{k}: {k.get_position()}")
k.move(1, 1)
print(f"{k}: {k.get_position()}")
k.move(3, 3)  # should be invalid move
print(f"{k}: {k.get_position()}")
k.move(2, 1)
print(f"{k}: {k.get_position()}")
k.move(1, 1)
print(f"{k}: {k.get_position()}")
k.move(0, 1)
print(f"{k}: {k.get_position()}")
k.move(-1, 1)  # should be invalid board placement
print(f"{k}: {k.get_position()}")
k.move(1, 1)
print(f"{k}: {k.get_position()}")

print('\nBishop Tests:')
b = Bishop(3, 0, -1)
print(f"Color: {b.get_color()}")
print(f"{b}: {b.get_position()}")
b.move(4, 1)
print(f"{b}: {b.get_position()}")
b.move(5, 2)
print(f"{b}: {b.get_position()}")
b.move(4, 1)
print(f"{b}: {b.get_position()}")
b.move(3, 1)  # should be invalid move
print(f"{b}: {b.get_position()}")
b.move(3, 2)
print(f"{b}: {b.get_position()}")
b.move(4, 3)
print(f"{b}: {b.get_position()}")
b.move(4, 1)  # should be invalid move
print(f"{b}: {b.get_position()}")

print('\nQueen Tests:')
q = Queen(0, 0, -1)
print(f"Color: {q.get_color()}")
print(f"{q}: {q.get_position()}")
q.move(7, 0)
print(f"{q}: {q.get_position()}")
q.move(7, 2)
print(f"{q}: {q.get_position()}")
q.move(6, 1)
print(f"{q}: {q.get_position()}")
q.move(4, 3)
print(f"{q}: {q.get_position()}")
q.move(5, 1)  # should be invalid move
print(f"{q}: {q.get_position()}")
q.move(5, 2)
print(f"{q}: {q.get_position()}")
q.move(9, 0)  # should be invalid board placement
print(f"{q}: {q.get_position()}")

print('\nKnight Tests:')
n = Knight(0, 0, 1)
print(f"Color: {n.get_color()}")
print(f"{n}: {n.get_position()}")
n.move(1, 2)
print(f"{n}: {n.get_position()}")
n.move(1, 3)  # should be invalid move
print(f"{n}: {n.get_position()}")
n.move(0, 4)
print(f"{n}: {n.get_position()}")
n.move(1, 6)
print(f"{n}: {n.get_position()}")
n.move(2, 6)  # should be invalid move
print(f"{n}: {n.get_position()}")
n.move(2, 4)
print(f"{n}: {n.get_position()}")
n.move(4, 5)
print(f"{n}: {n.get_position()}")
n.move(1, 9)  # should be invalid move
print(f"{n}: {n.get_position()}")
n.move(6, 6)
print(f"{n}: {n.get_position()}")


