
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
import functools
import copy


class AI:

    def __init__(self, color: int, mode: str):
        self._team = color
        self._legal_moves = []
        self.mode = mode  # "random", "basic", "medium", "advance"

    @staticmethod
    def scoring(board, color):
        """
        Generalized scoring system: score is positive if white is winning and negative if black
         is winning, the magnitude shows by how much one side is winning
        :param board: The board (represented as an 8x8 list of lists containing piece objects)
        :param color: The team of the side in question
        :return: A generalized score (int) for the difference in total piece worth for each side.
         """
        white = 0
        black = 0
        for i in range(8):  # for each row
            white += sum([piece.worth() for piece in board[i] if piece is not None and piece.get_color == 1])
            black += sum([piece.worth() for piece in board[i] if piece is not None and piece.get_color == -1])
        return (white - black) * color
    # TODO Update the worth of each piece as the game progresses, possibly move to board class

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
    def minimax(self, board, depth, maximizing_player, maximizing_color):
        """Implement minimax algorithm: the best move for the maximizing color looking ahead depth moves on the board
        :param board: The current board being evaluated
        :param depth: The current depth being evaluated
        :param maximizing_player: The team maximizing their score at the current depth
        :param maximizing_color: The team maximizing their score overall
        :return: A tuple with best move and best evaluation"""
        print(f'entering minimax w/ depth {depth}, maximizing player {maximizing_player}, and \
        maximizing color {maximizing_color}')
        b = board
        print(board)

        # base case: when depth = 0
        if depth == 0 or b.is_game_over():
            return None, self.scoring(board.get_board(), maximizing_color)

        moves = self.format_legal_moves(board)
        best_move = random.choice(moves)
        print(moves)

        min_or_max = maximizing_player * maximizing_color  # 1 if they are same (maximizing), -1 if they are different (minimizing)
        m_eval = -10000 * min_or_max  # large negative # if same (maximizing), large positive # if different (minimizing)
        for move in moves:
            b1 = copy.deepcopy(board)
            print(move[0], move[1])
            start, end = self.num_pos_to_letter_pos(move[0]), self.num_pos_to_letter_pos(move[1])
            print(start, end)
            b1.move_piece(start, end)
            curr_eval = self.minimax(b1, depth - 1, -1 * maximizing_player, maximizing_color)[1]
            if (curr_eval - m_eval) * min_or_max > 0:
                m_eval = curr_eval
                best_move = curr_eval
        return best_move, m_eval


    def make_move(self, board):
        """Choose (make a weighted choice) a move for the AI to make and make the move """
        moves_dict = {m: 1 for m in self._legal_moves}
        # .... # adjust weights according to AI decision making criteria
        if self.mode == "medium":
            self.minimax(board, 2, self._team, self._team)  # run minimax w/ depth 2
        else:
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
