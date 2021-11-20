
from board import Board
from AI import AI


def main():
    game = Board()
    ai = AI(-1, "full")
    game.start_game()
    turn(game, ai)


def turn(game, ai_game):
    while game.is_game_over() is False:
        # TODO change the game_over variable in board class once checkmate occurs
        print(game.__repr__())
        move(game, ai_game)
        game.switch_turn()
        turn(game, ai_game)
    # if end state is met (checkmate, forfeit)
    #   sys.exit(0)


def move(game: Board, game_ai: AI):
    if game.get_current_turn() == 1:
        print("White's turn.")
        mv_string = "Location of piece, ie A2: "
        ds_string = "Desired position, ie A3: "
    else:
        print("Black's turn.")
        mv_string = "Location of piece, ie A7: "
        ds_string = "Desired position, ie A6: "

    print(game.is_in_check(game.get_current_turn()))

    if game_ai.get_team() == game.get_current_turn():  # AI's turn
        game_ai.all_legal_moves(game)
        game_ai.make_move(game)
    else:
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
            print("move successful")
        except:  # This is far too general, but it is also not nearly finished
            print(game.__repr__())
            print('Redo move.')
            move(game, game_ai)


if __name__ == "__main__":
    main()
