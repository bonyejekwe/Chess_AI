
# TODO IDEAS:
#  *use the general scoring method to influence decision making for the AI
#  *implement a way to determine if a piece is in danger (possibly through piece or board class).
#  ****implement different game modes showing different stages of AI development (ie. "random", "basic", "medium", etc.)
#  -so far "basic" just favors capturing pieces of equal or lesser value, and favors not moving the king (need add more)
#  -so far "medium" is just basic minimax implemented, can use weighting to impact scoring

# TODO: The AI should retrieve all the information about its pieces to use (ie. every piece's position/color/worth/
#  in_danger status/etc). We can take the list of legal moves and take a weighted random choice, weighted by in_danger
#  status and other applicable factors

# TODO: in future mode, add to minimax (ideas: hardcode common chess openings/chess endings)


import random
from evaluate import Evaluation  # how to evaluate moves (to be implemented)
from pieces import *
from board import Board
import functools
import copy
from math import sqrt
from profiler import Profiler

class AI:

    def __init__(self, color: int, mode: str):
        self._team = color
        self._legal_moves = []
        self.mode = mode  # "random", "basic", "medium", "advance"

    @staticmethod
    @Profiler.profile
    def scoring(board: Board, color: int) -> int:
        """
        Generalized scoring system: score is positive if white is winning and negative if black
         is winning, the magnitude shows by how much one side is winning
        :param board: The board (represented as an 8x8 list of lists containing piece objects)
        :param color: The team of the side in question
        :return: A generalized score (int) for the difference in total piece worth for each side.
         """
        score = 0
        try:
            if board.checkmate(1):
                return -1 * float("inf")
            if board.checkmate(-1):
                return float("inf")
        except Board.NoKing:
            # print(board)
            pass

        # update scoring if a team is in check
#        if board.is_in_check(color):  # if you are in check
#            score -= 100
#        if board.is_in_check(-1 * color):  # if opponent is in check
#            score += 100

        white_pieces_left = board.get_pieces_left(1)
        black_pieces_left = board.get_pieces_left(-1)
        num_moves = board.get_current_move_count()

        # initial weighting: get the difference in worth for each team
        white = sum([30 * p.get_worth() for p in white_pieces_left])
        black = sum([30 * p.get_worth() for p in black_pieces_left])
        # print(white, black, (white - black) * color)
        score += (white - black) * color

        # TODO Update worth/use of each criteria wrt time (opening, endgame, etc.), possibly move to evaluation class
        # pawn development: increase score if pawns are moving up the board
        white = (1 / num_moves) * sum([4 * (p.get_position()[1] - p.original_position()[1]) for p in white_pieces_left
                                       if isinstance(p, Pawn)])
        black = (1 / num_moves) * sum([4 * (p.get_position()[1] - p.original_position()[1]) for p in black_pieces_left
                                       if isinstance(p, Pawn)])
        score += (white - black) * color

        # knight development: increase score if pawns are moving up the board
        white = (3 / num_moves) * sum([4 * (abs(2 - p.get_position()[1] + p.original_position()[1]))
                                       for p in white_pieces_left if isinstance(p, Knight)])
        black = (3 / num_moves) * sum([-4 * (abs(2 - p.get_position()[1] + p.original_position()[1]))
                                       for p in black_pieces_left if isinstance(p, Knight)])
        score += (white - black) * color

        # king development: increase score if king is not moving up the board
        white = sum([80 - (10 * (p.get_position()[1] - p.original_position()[1])) for p in white_pieces_left
                    if isinstance(p, King)])
        black = sum([80 + (10 * (p.get_position()[1] - p.original_position()[1])) for p in white_pieces_left
                    if isinstance(p, King)])
        score += (white - black) * color

        # general piece development: increase weight if pieces have many options to move
        white = 2 * sum([len(p.legal_moves()) for p in white_pieces_left if not isinstance(p, Pawn)])
        black = 2 * sum([len(p.legal_moves()) for p in black_pieces_left if not isinstance(p, Pawn)])
        score += (white - black) * color

        # favors opposing team's king in the corner
        try:
            if color == 1:
                black_king_x, black_king_y = board.get_king_position(-1)
                score += (board.get_current_move_count()/20) * (((black_king_x - 3)**2) + ((black_king_y - 3) ** 2)) * 20
            else:
                white_king_x, white_king_y = board.get_king_position(1)
                score -= (board.get_current_move_count()/20) * ((white_king_x - 3)**2) + ((white_king_y - 3) ** 2) * 20
        except Board.NoKing:
            pass

        return score

    def get_team(self):
        return self._team

    @staticmethod
    def format_legal_moves(board):
        """Retrieve the legal moves for the AI. Return as a list of tuples of tuples"""
        d = dict(board.legal_moves())  # key = piece position : values = list of possible next moves (tuples)
        for pos in d.keys():
            d[pos] = [(pos, val) for val in d[pos]]
        all_moves = functools.reduce(lambda l1, l2: l1 + l2, d.values())  # ((x1, y1), (x2, y2)): move: p1 -> p2
        return all_moves

    def all_legal_moves(self, board):
        """Set the formatted legal moves for the AI."""
        all_moves = self.format_legal_moves(board)
        self._legal_moves = all_moves

    @staticmethod
    def num_pos_to_letter_pos(position: tuple) -> tuple:
        """
        Converts a position like (0,0) to (A,1)
        :param position: Position you would like convert
        :return: A tuple with chess letter notation as position
        """
        return chr(position[0] + 65), position[1]+1  # a tuple

    # TODO need to make scoring more complex as many board positions will have the same score currently
    @Profiler.profile
    def minimax(self, board, depth, maximizing_player, maximizing_color):
        """Implement minimax algorithm: the best move for the maximizing color looking ahead depth moves on the board
        :param board: The current board being evaluated
        :param depth: The current depth being evaluated
        :param maximizing_player: The team maximizing their score at the current depth
        :param maximizing_color: The team maximizing their score overall
        :return: A tuple with best move and best evaluation"""
        # print(f'enter minimax w/ depth {depth}, maxim player {maximizing_player}, and maxim color {maximizing_color}')
        # b = board
        # print(board)

        # base case: when depth = 0
        if depth == 0 or board.is_game_over():
            return None, self.scoring(board, maximizing_color)

        moves = self.format_legal_moves(board)
        best_move = random.choice(moves)
        # print(moves)

        min_or_max = maximizing_player * maximizing_color  # 1 if they are same (maximizing), -1 if they are different (minimizing)
        m_eval = -10000 * min_or_max  # large negative # if same (maximizing), large positive # if different (minimizing)
        for move in moves:
            b1 = copy.deepcopy(board)
            # print(move[0], move[1])
            start, end = self.num_pos_to_letter_pos(move[0]), self.num_pos_to_letter_pos(move[1])
            # print(start, end)
            b1.move_piece(start, end)
            curr_eval = self.minimax(b1, depth - 1, -1 * maximizing_player, maximizing_color)[1]
            if (curr_eval - m_eval) * min_or_max > 0:
                m_eval = curr_eval
                best_move = move
        # print(best_move, m_eval)
        return best_move, m_eval

    @Profiler.profile
    def make_move(self, board):
        """Choose (make a weighted choice) a move for the AI to make and make the move """
        if self.mode == "medium":
            start_pos, end_pos = self.minimax(board, 2, self._team, self._team)[0]  # run minimax w/ depth 1
        else:
            moves_dict = {m: 1 for m in self._legal_moves}
            # adjust weights according to AI decision making criteria
            e = Evaluation(moves_dict, board)
            moves_dict = e.evaluated(self.mode)
            # make the move
            lis = [e for e in list(moves_dict.items())]
            moves, weights = [elem[0] for elem in lis], [elem[1] for elem in lis]
            if min(weights) < 0:
                weights = [num - min(weights) for num in weights]
            start_pos, end_pos = random.choices(moves, weights)[0]
        start_pos, end_pos = self.num_pos_to_letter_pos(start_pos), self.num_pos_to_letter_pos(end_pos)
        board.move_piece(start_pos, end_pos)  # move using chess letter notation
        print(f"moving from {start_pos} to {end_pos}")
        print(board)
