
# TODO IDEA: define a general scoring method (ie. for which side is winning
# TODO IDEA: create a AI that moves based on random moves generated from all possible legal moves
# TODO IDEA: somehow implement a way to determine if a piece is in danger (possibly through piece or board class).


# TODO IDEA: We can take the list of all legal moves and take a weighted random choice weighted by in_danger status and
# TODO IDEA: other factors that may apply


# TODO: The AI should be able to take in a state of the board, evaluate which side it is on, and
# TODO: retrieve all the information about its pieces to use (ie. every piece's position/color/worth/in_danger status)


import random
from board import Board


class AI:

    def __init__(self, color: int):
        self._team = color
        self._legal_moves = []

    @staticmethod
    def scoring(board):
        """Generalized scoring system: score is positive if white is winning and negative if black
         is winning, the magnitude shows by how much one side is winning"""
        # TODO Update the worth of each piece as the game progresses
        white = 0  # int: sum([ piece.get_worth() for piece in b if piece.get_color == 1 ])
        black = 0  # int: sum([ piece.get_worth() for piece in b if piece.get_color == -1 ])
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece is not None:
                    if piece.get_color == 1:
                        white += piece.get_worth()
                    elif piece.get_color == -1:
                        black += piece.get_worth()
        return white - black  # score positive if white winning, negative if black winning, magnitude shows by how much

    def get_team(self):
        return self._team

    def all_legal_moves(self, board):
        """Retrieve the state of the board and get all legal moves for the AI"""
        # TODO: IDEA: need to somehow retrieve the state of board and all pieces that are the same color as the board_color
        # b = [[]]  # retrieve the state of the board TODO implement this in some way
        c = -1  # (or 1, is the color of the AI)
        p = []  # [ piece for piece in b if piece.get_color == c ] # all pieces for the AI
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece.get_color == c:
                    p.append(piece)

        ai_legal_moves = []
        for piece in p:
            for move in piece.legal_moves():
                ai_legal_moves.append((piece.get_position(), move))  # ((x1, y1), (x2, y2)): move from 1 to 2

        self._legal_moves = ai_legal_moves

    def make_move(self, board):
        """Choose (make a weighted choice) a move for the AI to make and move"""
        moves = self._legal_moves
        move = random.choice(moves)
        # make move TODO implement a way for the AI to make a move specified as tuple of tuples (start_xy, end_xy)
        pass

b = Board()
b.start_game()
AI.scoring(b)

