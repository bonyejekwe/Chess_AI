
# game.py: play a player vs AI or an AI vs AI chess match

#  Currently each game is capped to take less than 200 moves and any game taking longer is listed as a timeout.
#  NOTE: the game code for performance.py: 1 = white checkmate win, -1 = black checkmate win, 2 = white
#  stalemated (black can't move), -2 = black stalemated (white can't move), 0 = draw, -5 = timeout (over 200 moves)

from board import Board
from AI import AI, MinimaxAI, MCTSAI
from profiler import Profiler


class InvalidModeError(Exception):
    def __init__(self, mode):
        super().__init__(f"Invalid Mode: {mode} is not a valid team. Must be either 1 or 2")


class InvalidTeamError(Exception):
    def __init__(self, team):
        super().__init__(f"Invalid Team: {team} is not a valid team. Must be either 1 or -1")


class InvalidAIType(Exception):
    def __init__(self, ty):
        super().__init__(f"Invalid AI Type: {ty} is not a valid team. Must be either 1, 2, 3, or 4")


class InvalidPositionError(Exception):
    def __init__(self, pos):
        super().__init__(f"Invalid Position: {pos} is not a valid position. Must be a letter, then a number")


def letter_pos_to_num_pos(pos: tuple) -> tuple:
    """
    Converts a position like (A,1) to (0,0)
    :param pos: Position you would like convert
    :return: A tuple with two numbers as position
    """
    return ord(pos[0]) - 65, pos[1] - 1
    # raise InvalidPositionError(pos):


def main():
    winners = []
    for _ in range(1):
        result = run_game()  # run AI vs AI (change argument to 1 for player vs AI)
        winners.append(result)
        Profiler.report()
    print("Winners", winners)


def play_game():
    """Play a game against an AI"""
    board = Board()

    # Get the side from the player
    side = input("Select side you would like to play on (1 for white, -1 for black): ")
    if side == "1" or side == "-1":
        side = int(side)
    else:
        raise InvalidTeamError(side)

    ai_team = -1 * side  # Set the ai's side

    # Get the desired AI type and define AI
    ai_types = {0: AI, 1: MinimaxAI, 2: MCTSAI}
    ai_type = input("Select AI to play against {0: AI, 1: MinimaxAI, 2: MCTSAI}: ")
    if ai_type == "0" or ai_type == "1" or ai_type == "2":
        ai_type = ai_types[int(ai_type)]
        ai = ai_type(ai_team)  # define the AI
    else:
        raise InvalidAIType(ai_type)

    if side == 1:  # [user, ai]
        ai_lis = [None, ai]
    else:  # side == -1,  [ai, user]
        ai_lis = [ai, None]

    board.start_game()
    game_winner = turn(board, ai_lis)  # run the game
    print("the winner is...", game_winner)
    return game_winner


def run_simulation():
    """Run an AI vs AI simulation"""
    board = Board()

    # Get the desired AI type and define AI
    ai_types = {0: AI, 1: MinimaxAI, 2: MCTSAI}
    ai_type = input("Select AI to play as white {0: AI, 1: MinimaxAI, 2: MCTSAI}: ")
    if ai_type == "0" or ai_type == "1" or ai_type == "2":
        ai_type = ai_types[int(ai_type)]
        ai_white = ai_type(1)  # define the AI
    else:
        raise InvalidAIType(ai_type)

    ai_type = input("Select AI to play as black {0: AI, 1: MinimaxAI, 2: MCTSAI}: ")
    if ai_type == "0" or ai_type == "1" or ai_type == "2":
        ai_type = ai_types[int(ai_type)]
        ai_black = ai_type(-1)  # define the AI
    else:
        raise InvalidAIType(ai_type)

    ai_lis = [ai_white, ai_black]

    board.start_game()
    game_winner = turn(board, ai_lis)  # run the game
    print("the winner is...", game_winner)
    return game_winner
    pass


@Profiler.profile
def run_game():
    """Start a game using num of AI's (1=player vs AI, 2=AI vs AI). Defaults to AI vs AI"""
    mode = input("number of AI's: (1 to play against AI, 2 for AI vs AI simulation : ")

    if mode == "1":
        return play_game()
    elif mode == "2":
        return run_simulation()
    else:
        raise InvalidModeError(mode)


@Profiler.profile
def turn(board, ai_lis):  # defaults to no AI for game
    """Run the actual game"""
    while not board.is_game_over():
        move(board, ai_lis)
        board.switch_turn()
        print(f"Turn #: {board.get_current_move_count()}...")

    return board.winner()


def move(game: Board, ai_lis):
    """Complete a move, either from a user or the AI"""

    if game.get_current_turn() == 1:  # white to move
        print("White's turn.")
        mv_string = "Location of piece, ie A2: "
        ds_string = "Desired position, ie A3: "
        idx = 0
    else:  # black to move
        print("Black's turn.")
        mv_string = "Location of piece, ie A7: "
        ds_string = "Desired position, ie A6: "
        idx = 1

    if game.is_in_check(game.get_current_turn()):
        for _ in range(10):
            print(f'{game.get_current_turn()} is in check!!!')

    if ai_lis[idx] is not None:  # an AI turn
        ai = ai_lis[idx]
        ai.make_move(game)
    else:  # user turn
        # take positions from input
        moving_piece = list(input(mv_string))
        moving_piece[0] = moving_piece[0].upper()
        moving_piece[1] = int(moving_piece[1])
        moving_piece = tuple(moving_piece)
        desired_position = list(input(ds_string))
        desired_position[0] = desired_position[0].upper()
        desired_position[1] = int(desired_position[1])
        desired_position = tuple(desired_position)
        print(moving_piece)
        print(desired_position)
        pos1, pos2 = letter_pos_to_num_pos(moving_piece), letter_pos_to_num_pos(desired_position)

        # need error check tuples, a-h, 1-8, len = 2, custom exceptions
        try:
            game.move_piece(pos1, pos2)
            print("move successful")
        except:  # This is far too general, but it is also not nearly finished
            print(game.__repr__())
            print('Redo move.')
            move(game, ai_lis)


if __name__ == "__main__":
    main()

