
from board import Board


def loop(bd):
    for _ in range(10):
        print("Actual!!!!!")
    print(bd)
    bd.switch_turn()
    print('d', bd.is_in_check(bd.get_current_turn()))
    print(bd.legal_moves())


def main():
    b = Board()
    b.start_game()
    print(b.is_in_check(b.get_current_turn()))
    print(b)
    b.move_piece(('C', 2), ('C', 4))
    loop(b)
    b.move_piece(('D', 7), ('D', 5))
    loop(b)
    b.move_piece(('D', 2), ('D', 4))
    loop(b)
    b.move_piece(('E', 7), ('E', 5))
    loop(b)
    b.move_piece(('D', 1), ('A', 4))
    loop(b)
    b.move_piece(('B', 8), ('D', 7))
    loop(b)
    b.move_piece(('G', 2), ('G', 3))
    loop(b)


if __name__ == "__main__":
    main()
