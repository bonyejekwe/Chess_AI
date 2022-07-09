
# AI.py: our chess AI

#  -"basic" just favors capturing pieces of equal or lesser value, and favors not moving the king (need add more)
#  -"medium" is minimax implemented (w/ alpha beta pruning), using AI scoring criteria

import random
from pieces import *
from board import Board
import functools
from profiler import Profiler


class AI:

    def __init__(self, color: int, mode: str):
        self._team = color
        self._legal_moves = []
        self.mode = mode  # "random" or "medium",
        self.alpha = -999999999
        self.beta = 999999999

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
        try:
            if board.checkmate(1):
                return -99999999
            if board.checkmate(-1):
                return 99999999
        except Board.NoKing:
            print(board)
            pass

        scores = []  # [white score, black score]
        num_moves = board.get_current_move_count()
        for team in [1, -1]:
            consider = board.get_pieces_left(team)  # white_pieces_left, then black_pieces_left

            worth_weights = []  # initial weighting: get the difference in worth for each team
            pawn_development = []  # pawn development: increase score if pawns are moving up the board
            knight_development = []  # knight development: increase score if pawns are moving up the board
            king_development = []  # king development: increase score if king is not moving up the board
            piece_development = []  # general piece development: increase weight if pieces have many options to move

            for p in consider:
                if isinstance(p, Pawn):
                    pawn_development.append(5 * (p.get_position()[1] - 1))
                else:
                    if isinstance(p, Knight):
                        knight_development.append(20 * (5 - abs(3 - p.get_position()[1])))
                    elif isinstance(p, King):
                        king_development.append(80 - (10 * (p.get_position()[1] - p.original_position()[1])))
                    piece_development.append(len(p.legal_moves()))
                worth_weights.append(50 * p.get_worth())

            score = sum(worth_weights)
            score += ((sum(pawn_development) + sum(knight_development)) / num_moves) + (sum(king_development)) + (
                    15 * sum(piece_development))
            scores.append(score)

        return scores[0] - scores[1]  # white_score - black_score

    def get_team(self):
        """:return: The team the AI is"""
        return self._team

    @staticmethod
    def format_legal_moves(board: Board):
        """Retrieve the legal moves for the AI. Return as a list of tuples of tuples. Takes as input a board object."""
        d = dict(board.legal_moves())  # key = piece position : values = list of possible next moves (tuples)
        for pos in d:
            d[pos] = [(pos, val) for val in d[pos]]
        all_moves = functools.reduce(lambda l1, l2: l1 + l2, d.values())  # ((x1, y1), (x2, y2)): move: p1 -> p2
        return all_moves

    def all_legal_moves(self, board: Board):
        """Set the formatted legal moves for the AI. Takes as input a board object"""
        all_moves = self.format_legal_moves(board)
        self._legal_moves = all_moves

    @staticmethod
    def num_pos_to_letter_pos(position: tuple) -> tuple:
        """
        Converts a position like (0,0) to (A,1)
        :param position: Position you would like convert
        :return: A tuple with chess letter notation as position
        """
        return chr(position[0] + 65), position[1] + 1  # a tuple

    @Profiler.profile
    def minimax(self, board: Board, depth: int, maximizing_player: int, maximizing_color: int):
        """Implement minimax algorithm: the best move for the maximizing color looking ahead depth moves on the board
        :param board: The current board being evaluated
        :param depth: The current depth being evaluated
        :param maximizing_player: The team maximizing their score at the current depth
        :param maximizing_color: The team maximizing their score overall
        :return: A tuple with best move and best evaluation"""

        # base case: depth = 0
        if depth == 0 or board.is_game_over():
            board._game_over = False
            return None, self.scoring(board, maximizing_color)

        moves = self.format_legal_moves(board)
        best_move = moves[0]

        min_or_max = maximizing_player * maximizing_color  # 1 if same (maximizing), -1 if different (minimizing)
        m_eval = -10000 * min_or_max  # large negative if same (maximizing), large positive if different (minimizing)
        for move in moves:
            # make the move on the board
            piece1, piece2 = board.get_piece_from_position(move[0]), board.get_board()[move[1][1]][move[1][0]]
            pos1x, pos1y, pos2x, pos2y = move[0][0], move[0][1], move[1][0], move[1][1]
            board.update_pieces(piece1, pos2x, pos2y)
            if isinstance(piece2, Piece):  # temporarily delete piece from dict if necessary
                board.update_pieces(piece2, pos2x, pos2y, delete=True)
            board.get_board()[pos1y][pos1x], board.get_board()[pos2y][pos2x] = None, board.get_board()[pos1y][pos1x]
            board.update_move_count()
            board.switch_turn()

            # make a recursive call to minimax to find the best evaluation at a specified depth
            curr_eval = self.minimax(board, depth - 1, -1 * maximizing_player, maximizing_color)[1]

            # unmake the move on the board
            board.switch_turn()
            board.update_pieces(piece1, pos1x, pos1y, revert=True)  # unmake the temporary move
            if isinstance(piece2, Piece):  # add back piece to dict if necessary
                board.update_pieces(piece2, pos2x, pos2y, adding=True)
            board.get_board()[pos1y][pos1x], board.get_board()[pos2y][pos2x] = board.get_board()[pos2y][pos2x], piece2
            board.update_move_count(False)

            # update the best found move and score if necessary
            if min_or_max == 1:
                if self.alpha == -999999999:
                    self.alpha = curr_eval
                if curr_eval > self.alpha:
                    self.alpha = curr_eval
                if self.beta > self.alpha and self.beta != 999999999:
                    print('Time saved!!!! b>a')
                    break
            else:
                if self.beta == 999999999:
                    self.beta = curr_eval
                if curr_eval < self.beta:
                    self.beta = curr_eval
                if self.alpha < self.beta and self.alpha != -999999999:
                    break

            if min_or_max == 1:
                if curr_eval > m_eval:
                    m_eval = curr_eval
                    best_move = move
            else:
                if curr_eval < m_eval:
                    m_eval = curr_eval
                    best_move = move

        return best_move, m_eval

    @Profiler.profile
    def make_move(self, board: Board):
        """Choose (make a weighted choice) a move for the AI to make and make the move. Takes as input a board object"""
        if self.mode == "medium":
            if self._team == 1:
                start_pos, end_pos = self.minimax(board, 3, 1, 1)[0]  # minimax
            elif self._team == -1:
                start_pos, end_pos = self.minimax(board, 3, 1, -1)[0]  # minimax
            self.alpha = -999999999
            self.beta = 999999999
        else:
            moves_dict = {m: 1 for m in self._legal_moves}
            lis = [e for e in list(moves_dict.items())]
            moves, weights = [elem[0] for elem in lis], [elem[1] for elem in lis]
            if min(weights) < 0:
                weights = [num - min(weights) for num in weights]
            start_pos, end_pos = random.choices(moves, weights)[0]
        start_pos, end_pos = self.num_pos_to_letter_pos(start_pos), self.num_pos_to_letter_pos(end_pos)
        board.move_piece(start_pos, end_pos)  # move using chess letter notation
        print(f"moving from {start_pos} to {end_pos}")
        print(board)
