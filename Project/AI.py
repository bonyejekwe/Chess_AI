
# TODO IDEAS:
#  *implement a way to determine if a piece is in danger (possibly through piece or board class).
#  -"basic" just favors capturing pieces of equal or lesser value, and favors not moving the king (need add more)
#  -"medium" is minimax implemented (w/ alpha beta pruning), using AI scoring criteria

# TODO: The AI should retrieve all the information about its pieces to use (ie. every piece's position/color/worth/
#  in_danger status/etc).

# TODO: in future mode, potentially add hardcode common chess openings/chess endings


import random
from evaluate import Evaluation  # how to evaluate moves (to be implemented)
from pieces import *
from board import Board
import functools
from profiler import Profiler


class AI:

    def __init__(self, color: int, mode: str):
        self._team = color
        self._legal_moves = []
        self.mode = mode  # "random", "basic", "medium", "advance"
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
        score = 0
        try:
            if board.checkmate(1):
                return -99999999
            if board.checkmate(-1):
                return 99999999
        except Board.NoKing:
            print(board)
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
        white = sum([p.get_worth() for p in white_pieces_left])
        black = sum([p.get_worth() for p in black_pieces_left])
        score += (white - black)
        white_score = 0
        black_score = 0
        # TODO Update worth/use of each criteria wrt time (opening, endgame, etc.), possibly move to evaluation class

        # pawn development: increase score if pawns are moving up the board
        white_score += sum([5 * (p.get_position()[1] - 1) for p in white_pieces_left if isinstance(p, Pawn)]) / num_moves
        # knight development: increase score if pawns are moving up the board
        white_score += sum([20 * (5 - abs(3 - p.get_position()[1])) for p in white_pieces_left if isinstance(p, Knight)]) / num_moves
        # king development: increase score if king is not moving up the board
        white_score += sum([80 - (10 * (p.get_position()[1] - p.original_position()[1])) for p in white_pieces_left if isinstance(p, King)])
        # general piece development: increase weight if pieces have many options to move
        white_score += 15 * sum([len(p.legal_moves()) for p in white_pieces_left if not isinstance(p, Pawn)])
#
        # black
        # pawn development: increase score if pawns are moving up the board
        black_score += sum([5 * (6 - p.get_position()[1]) for p in black_pieces_left if isinstance(p, Pawn)]) / num_moves
        # knight development: increase score if pawns are moving up the board
        black_score += sum([20 * (5 - abs(4 - p.get_position()[1])) for p in black_pieces_left if isinstance(p, Knight)]) / num_moves
        # king development: increase score if king is not moving up the board
        black_score += sum([80 + (10 * (p.get_position()[1] - p.original_position()[1])) for p in black_pieces_left if isinstance(p, King)])
        # general piece development: increase weight if pieces have many options to move
        black_score += 15 * sum([len(p.legal_moves()) for p in black_pieces_left if not isinstance(p, Pawn)])

        # favors opposing team's king in the corner
        #try:
        #    if color == 1:
        #        black_king_x, black_king_y = board.get_king_position(-1)
        #        score += (board.get_current_move_count()/20) * (((black_king_x - 3)**2) + ((black_king_y - 3) ** 2)) * 20
        #    else:
        #        white_king_x, white_king_y = board.get_king_position(1)
        #        score -= (board.get_current_move_count()/20) * ((white_king_x - 3)**2) + ((white_king_y - 3) ** 2) * 20
        #except Board.NoKing:
        #    pass
        score += (white_score-black_score)
        return score

    def get_team(self):
        return self._team

    @staticmethod
    def format_legal_moves(board: Board):
        """Retrieve the legal moves for the AI. Return as a list of tuples of tuples"""
        d = dict(board.legal_moves())  # key = piece position : values = list of possible next moves (tuples)
        for pos in d:
            d[pos] = [(pos, val) for val in d[pos]]
        all_moves = functools.reduce(lambda l1, l2: l1 + l2, d.values())  # ((x1, y1), (x2, y2)): move: p1 -> p2
        return all_moves

    def all_legal_moves(self, board: Board):
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
        return chr(position[0] + 65), position[1] + 1  # a tuple

    # TODO need to make scoring more complex as many board positions will have the same score currently
    @Profiler.profile
    def minimax(self, board, depth, maximizing_player, maximizing_color):
        """Implement minimax algorithm: the best move for the maximizing color looking ahead depth moves on the board
        :param board: The current board being evaluated
        :param depth: The current depth being evaluated
        :param maximizing_player: The team maximizing their score at the current depth
        :param maximizing_color: The team maximizing their score overall
        :return: A tuple with best move and best evaluation"""

        # base case: depth = 0
        if depth == 0 or board.is_game_over():
            return None, self.scoring(board, maximizing_color)

        moves = self.format_legal_moves(board)
        random.shuffle(moves)
        best_move = moves[0]

        min_or_max = maximizing_player * maximizing_color  # 1 if they are same (maximizing), -1 if they are different (minimizing)
        m_eval = -10000 * min_or_max  # large negative # if same (maximizing), large positive # if different (minimizing)
        for move in moves:
            # make the move on the board
            piece1, piece2 = board.get_piece_from_position(move[0]), board.get_board()[move[1][1]][move[1][0]]
            pos1x, pos1y, pos2x, pos2y = move[0][0], move[0][1], move[1][0], move[1][1]
            board.update_pieces(piece1, pos2x, pos2y)
            if isinstance(piece2, Piece):  # temporarily delete piece from dict if necessary
                board.update_pieces(piece2, pos2x, pos2y, delete=True)
            board.get_board()[pos1y][pos1x], board.get_board()[pos2y][pos2x] = None, board.get_board()[pos1y][pos1x]
            board._move_count += 1
            board.switch_turn()

            # make a recursive call to minimax to find the best evaluation at a specified depth
            curr_eval = self.minimax(board, depth - 1, -1 * maximizing_player, maximizing_color)[1]

            # unmake the move on the board
            board.switch_turn()
            board.update_pieces(piece1, pos1x, pos1y, revert=True)  # unmake the temporary move
            if isinstance(piece2, Piece):  # add back piece to dict if necessary
                board.update_pieces(piece2, pos2x, pos2y, adding=True)
            board.get_board()[pos1y][pos1x], board.get_board()[pos2y][pos2x] = board.get_board()[pos2y][pos2x], piece2
            board._move_count -= 1

            # update the best found move and score if necessary
            if min_or_max == 1:
                if self.alpha == -999999999:
                    self.alpha = curr_eval
                print('maximizing!!', min_or_max, curr_eval, "alpha: ", self.alpha, 'beta: ', self.beta, 'move: ', (self.num_pos_to_letter_pos(move[0]), self.num_pos_to_letter_pos(move[1])))
                if curr_eval > self.alpha:
                    self.alpha = curr_eval
                if self.beta > self.alpha and self.beta != 999999999:
                    print('Time saved!!!! b>a')
                    break
            else:
                if self.beta == 999999999:
                    self.beta = curr_eval
                print('minimizing!!', min_or_max, curr_eval, "alpha: ", self.alpha, 'beta : ', self.beta,'move: ', (self.num_pos_to_letter_pos(move[0]), self.num_pos_to_letter_pos(move[1])))
                if curr_eval < self.beta:
                    self.beta = curr_eval
                if self.alpha < self.beta and self.alpha != -999999999:
                    print('Time saved!!!! a<b')
                    break

            if (curr_eval - m_eval) * min_or_max > 0:
                m_eval = curr_eval
                best_move = move

        # print(depth, best_move, m_eval)
        return best_move, m_eval

    @Profiler.profile
    def make_move(self, board: Board):
        """Choose (make a weighted choice) a move for the AI to make and make the move """
        if self.mode == "medium":
            if self._team == 1:
                start_pos, end_pos = self.minimax(board, 2, 1, 1)[0]  # minimax
            elif self._team == -1:
                start_pos, end_pos = self.minimax(board, 2, 1, -1)[0]  # minimax
            self.alpha = -999999999
            self.beta = 999999999
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
