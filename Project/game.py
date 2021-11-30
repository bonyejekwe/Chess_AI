
# TODO README!!!!
#  Currently each game is capped to take less than 200 moves and any game taking longer is listed as a timeout.
#  NOTE: this can be changed, but game code for performance.py: 1= white checkmate win, -1=black checkmate win, 2=white
#  stalemated (black can't move), -2=black stalemated (white can't move), 0=draw?, -5=timeout (over 200 moves)

from board import Board
from AI import AI


def main():
    winners = []
    for _ in range(7):
        result = run_game(2, mode1='medium')  # run AI vs AI (change argument to 1 for player vs AI)
        winners.append(result)
    print("Winners", winners)


def run_game(num=2, mode1="random", mode2="random"):
    """Run game using num of AI's (1=player vs AI, 2=AI vs AI). Defaults to AI vs AI"""
    game = Board()
    if num == 1:  # player against ai
        side = int(input("Select side you would like to play on (1 for white, -1 for black): "))
        ai_team = -1 * side
        ai = AI(ai_team, mode1)
        ai2 = False
    else:
        ai = AI(1, mode1)
        ai2 = AI(-1, mode2)
    game.start_game()
    game_winner = turn(game, ai, ai2)  # run the game
    print("the winner is...", game_winner)
    return game_winner


def turn(game, ai_game, ai_game2=False):  # effectively defaults to no AI for game
    timed_out = -5
    while game.is_game_over() is False and game.get_current_move_count() < 200:
        move(game, ai_game, ai_game2)
        game.switch_turn()
        print(f"Turn #: {game.get_current_move_count()}...")
        # print(f"captured: {[str(p) for p in game.get_captured()]}")
    if game.is_game_over():
        return game.winner()
    else:
        print('timed out')
        return timed_out


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
