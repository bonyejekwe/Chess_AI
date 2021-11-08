from board import Board


def main():
    game = Board()
    game.start_game()
    turn(game)


def turn(game):
    # this should probably recurse to maintain the game and break out when on an end state
    print(game.__repr__())

    # if end state is met (checkmate, forfeit)
    #   sys.exit(0)

    # recurse
    move(game)
    game.switch_turn()
    turn(game)


def move(game):
    if game._turn == 1:
        print("White's turn.")
        mv_string = "Location of piece, ie A2: "
        ds_string = "Desired position, ie A3: "
    else:
        print("Black's turn.")
        mv_string = "Location of piece, ie A7: "
        ds_string = "Desired position, ie A6: "

    # take positions from input
    moving_piece = list(input(mv_string))
    moving_piece[0] = moving_piece[0].upper()
    moving_piece[1] = int(moving_piece[1])
    moving_piece = tuple(moving_piece)
    desired_position = list(input(ds_string))
    desired_position[0] = desired_position[0].upper()
    desired_position[1] = int(desired_position[1])
    desired_position = tuple(desired_position)
    # need error check tuples, a-h, 1-8, len = 2, custom exceptions
    try:
        game.move_piece(moving_piece, desired_position)
    except:  # This is far too general, but it is also not nearly finished
        print(game.__repr__())
        print('Redo move.')
        move(game)


if __name__ == "__main__":
    main()
