
from board import Board
from pieces import *


class Evaluation:

    def __init__(self, moves, board):
        self.moves = moves  # dict {move: weight for all legal moves}
        self.board = board.get_board()

    # TODO define functions evaluating different types of criteria
    # example basic functions:
    def capture(self):
        """Increases weight if move will be capturing piece of lower worth"""
        moves = self.moves
        for move, weight in moves.items():
            s, e = move[0], move[1]
            p1 = self.board[s[0]][s[1]]
            p2 = self.board[e[0]][e[1]]
            if isinstance(p1, Piece) and isinstance(p2, Piece):
                if p1.get_worth() >= p2.get_worth():
                    moves[move] += 10
        self.moves = moves

    def king_restrict(self):
        """Decreases weight if involves king movement"""
        moves = self.moves
        for move, weight in moves.items():
            s, e = move[0], move[1]
            if isinstance(self.board[s[0]][s[1]], King):
                moves[move] -= 3
        self.moves = moves

    # example medium functions:
    # .....

    # AI mode function calls
    @staticmethod
    def random():
        """Evaluate using random mode"""
        return 0

    def basic(self):
        """Evaluate using basic mode"""
        self.capture()
        self.king_restrict()
        return 0

    def func_call(self, func_name):
        funcs = {'random': self.random, 'basic': self.basic}  # add medium, hard, etc.
        func = funcs[func_name]
        func()

    def evaluated(self, func_name):
        """Return the list (or dict) of moves mapped to corresponding weights after evaluation"""
        self.func_call(func_name)
        return self.moves

