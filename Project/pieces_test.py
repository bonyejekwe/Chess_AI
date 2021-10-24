
from pieces import *

# Tests
print('Rook Tests:')
r = Rook(0, 0, -1)  # 0 = "black"
print(r)
r.move(3, 0)
print(r)
r.move(7, 3)  # should be invalid move
print(r)
r.move(3, 3)
print(r)
r.move(9, 3)  # should be invalid board placement
print(r)

print('\nKing Tests:')
k = King(0, 0, 1)  # 1 = "white"
print(k)
k.move(1, 1)
print(k)
k.move(3, 3)  # should be invalid move
print(k)
k.move(2, 1)
print(k)
k.move(1, 1)
print(k)
k.move(0, 1)
print(k)
k.move(-1, 1)  # should be invalid board placement
print(k)
k.move(1, 1)
print(k)

print('\nBishop Tests:')
b = Bishop(3, 0, -1)
print(b)
b.move(4, 1)
print(b)
b.move(5, 2)
print(b)
b.move(4, 1)
print(b)
b.move(3, 1)  # should be invalid move
print(b)
b.move(3, 2)
print(b)
b.move(4, 3)
print(b)
b.move(4, 1)  # should be invalid move
print(b)

print('\nQueen Tests:')
q = Queen(0, 0, -1)
print(q)
q.move(7, 0)
print(q)
q.move(7, 2)
print(q)
q.move(6, 1)
print(q)
q.move(4, 3)
print(q)
q.move(5, 1)  # should be invalid move
print(q)
q.move(5, 2)
print(q)
q.move(9, 0)  # should be invalid board placement
print(q)

print('\nKnight Tests:')
n = Knight(0, 0, 1)
print(n)
n.move(1, 2)
print(n)
n.move(1, 3)  # should be invalid move
print(n)
n.move(0, 4)
print(n)
n.move(1, 6)
print(n)
n.move(2, 6)  # should be invalid move
print(n)
n.move(2, 4)
print(n)
n.move(4, 5)
print(n)
n.move(1, 9)  # should be invalid move
print(n)
n.move(6, 6)
print(n)


print('\n')


board_test = [0] * 8

print(board_test)
print(board_test)
print(board_test)
print(board_test)
print(board_test)
print([0, 0, 0, 1, 0, 0, 0, 0])
print(board_test)
print(board_test)
