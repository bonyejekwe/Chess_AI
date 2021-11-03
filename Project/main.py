from board import Board
from pieces import *

def main():
    b = Board()
    b.start_game()
    print(b)
    b.move_piece(('A',2), ('A',3))
    b.move_piece(('B',1), ('B',3))
    print(b)

if __name__ == "__main__":
    main()