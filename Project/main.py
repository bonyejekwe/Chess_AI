from board import Board
from pieces import *

def main():
    b = Board()
    b.start_game()
    print(b)
    b.move_piece(('A',2), ('A',3))
    b.move_piece(('B',1), ('C',3))
    b.switch_turn()
    print("Rook capture")
    b.move_piece(('A',8), ('A',3))
    print(b)
    print(b.get_captured())

if __name__ == "__main__":
    main()