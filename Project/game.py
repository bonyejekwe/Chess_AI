
# TODO README!!!!
#  Still need to implement checkmate in the game correctly. Currently the game does end at a point that very closely
#  resembles checkmate but there is probably a bug somewhere. Also, a lot of the games end in "draws"
#  (currently each game is capped to take less than 200 moves and any game taking longer is listed as a
#  draw. The endgame is a major problem (ie. when there's just two kings randomly moving, etc.), so implementing like
#  the 3fold repetition or something like the 50-move w/o capture rule would help

from board import Board
from AI import AI


def main():
    winners = []
    for _ in range(10):
        result = run_game(2)  # run AI vs AI (change argument to 1 for player vs AI)
        winners.append(result)
    print("Winners", winners)


def run_game(num=2):
    """Run game using num of AI's (1=player vs AI, 2=AI vs AI). Defaults to AI vs AI"""
    game = Board()
    if num == 1:  # player against ai
        side = int(input("Select side you would like to play on (1 for white, -1 for black): "))
        ai_team = -1 * side
        ai = AI(ai_team, "medium")
        ai2 = False
    else:
        ai = AI(-1, "random")
        ai2 = AI(1, "medium")
    game.start_game()
    game_winner = turn(game, ai, ai2)  # run the game
    print("the winner is...", game_winner)
    return game_winner


def turn(game, ai_game, ai_game2=False):  # effectively defaults to no AI for game
    i = 0
    # print(game.__repr__())
    win = 0
    while game.is_game_over() is False and i < 200:
        # TODO change the game_over variable in board class once checkmate occurs
        move(game, ai_game, ai_game2)
        game.switch_turn()
        # turn(game, ai_game, ai_game2)
        i += 1
        for _ in range(10):
            print(f"Turn #: {i}...")
        # print(f'captured: {[str(p) for p in game.get_captured()]}')
        # print(game.__repr__())
    if game.is_game_over():
        return game.winner()
    else:
        return win
    # if end state is met (checkmate, forfeit)
    #   sys.exit(0)


def move(game: Board, game_ai: AI, game_ai2=False):
    if game.get_current_turn() == 1:
        print("White's turn.")
        mv_string = "Location of piece, ie A2: "
        ds_string = "Desired position, ie A3: "
    else:
        print("Black's turn.")
        mv_string = "Location of piece, ie A7: "
        ds_string = "Desired position, ie A6: "

    if game.is_in_check(game.get_current_turn()):
        for _ in range(10):
            print(f'{game.get_current_turn()} is in check!!!')

    if game_ai.get_team() == game.get_current_turn():  # AI's turn
        game_ai.all_legal_moves(game)
        game_ai.make_move(game)
    elif game_ai2:
        if game_ai2.get_team() == game.get_current_turn():  # AI's turn
            game_ai2.all_legal_moves(game)
            game_ai2.make_move(game)
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
            move(game, game_ai, game_ai2)


if __name__ == "__main__":
    main()
