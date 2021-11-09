
from board import Board

board = Board()
board.start_game()
print(board)
board.move_piece(('B', 1), ('A', 3))
print(board)
# board.move_piece(('D', 7), ('D', 6))
# print(board)
# board.move_piece(('E', 2), ('E', 4))
# print(board)
