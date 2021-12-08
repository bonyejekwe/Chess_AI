
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
    b._start_test_game()
    print(b)
    print(b.legal_moves())
    b.switch_turn()
    print(b.legal_moves())
    b.move_piece(('H',8),('H',7))
    print(b)




if __name__ == "__main__":
    main()
