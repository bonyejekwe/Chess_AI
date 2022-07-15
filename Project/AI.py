
# AI.py: our chess AI

#  -"basic" just favors capturing pieces of equal or lesser value, and favors not moving the king (need add more)
#  -"medium" is minimax implemented (w/ alpha beta pruning), using AI scoring criteria

import copy
import time
import math
import random
from pieces import *
from board import Board, NoKingError
from profiler import Profiler


class AI:

    def __init__(self, color: int):
        self._team = color
        self._legal_moves = []

    @staticmethod
    # @Profiler.profile
    def scoring(board: Board, color: int) -> int:
        """
        Generalized scoring system: score is positive if white is winning and negative if black
         is winning, the magnitude shows by how much one side is winning
        :param board: The board (represented as an 8x8 list of lists containing piece objects)
        :param color: The team of the side in question
        :return: A generalized score (int) for the difference in total piece worth for each side.
         """
        try:
            if board.checkmate():
                return -99999999 * board.get_current_turn()  # large negative if white in checkmate, positive if black

        except NoKingError:
            print(board)
            pass

        scores = []  # [white score, black score]
        num_moves = board.get_current_move_count()
        for team in [1, -1]:
            consider = board.get_pieces_left(color * team)  # pieces left for AI, then pieces left for other team

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

        return scores[0] - scores[1]  # AI score - other score

    def get_team(self):
        """:return: The team the AI is"""
        return self._team

    @staticmethod
    def format_legal_moves(board: Board):
        """Retrieve the legal moves for the AI. Return as a list of tuples of tuples. Takes as input a board object."""
        all_moves = []
        d = board.legal_moves()  # key = piece position : values = list of possible next moves (tuples)
        for pos in d:
            all_moves += [(pos, val) for val in d[pos]]  # ((x1, y1), (x2, y2)): move: p1 -> p2
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
    def make_move(self, board: Board):
        """Choose (make a weighted choice) a move for the AI to make and make the move. Takes as input a board object"""
        moves_dict = {m: 1 for m in self._legal_moves}
        lis = [e for e in list(moves_dict.items())]
        moves, weights = [elem[0] for elem in lis], [elem[1] for elem in lis]
        if min(weights) < 0:
            weights = [num - min(weights) for num in weights]
        start_pos, end_pos = random.choices(moves, weights)[0]
        board.move_piece(start_pos, end_pos)  # move using chess letter notation
        print(f"moving from {start_pos} to {end_pos}")
        print(board)


class MinimaxAI(AI):

    def __init__(self, color: int):
        super().__init__(color)
        self.alpha = -1 * float('inf')
        self.beta = float('inf')
        self.max_depth = 3

    @Profiler.profile
    def minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool):
        """Implement minimax algorithm: the best move for the maximizing color looking ahead depth moves on the board
        :param board: The current board being evaluated
        :param depth: The current depth being evaluated
        :param alpha: value for alpha
        :param beta: value for beta
        :param maximizing_player: bool representing whether the AI's team is maximizing their score at the current depth
        :return: A tuple with best move and best evaluation"""
        # base case: depth = 0
        if depth == 0 or board.is_game_over():
            board._game_over = False
            return None, self.scoring(board, self._team)

        moves = self.format_legal_moves(board)
        best_move = moves[0]

        if maximizing_player:
            max_eval = -1 * float('inf')
            for move in moves:
                # make the move on the board
                board.move_piece(move[0], move[1], check=False)
                board.switch_turn()

                # make a recursive call to minimax to find the best evaluation at a specified depth
                curr_eval = self.minimax(board, depth - 1, alpha, beta, False)[1]

                # unmake the move on the board
                board.undo_move()
                board.switch_turn()

                if curr_eval > max_eval:
                    max_eval = curr_eval
                    best_move = move

                alpha = max(alpha, curr_eval)

                if beta <= alpha:
                    break
            return best_move, max_eval

        else:
            min_eval = float('inf')
            for move in moves:
                # make the move on the board
                board.move_piece(move[0], move[1], check=False)
                board.switch_turn()

                # make a recursive call to minimax to find the best evaluation at a specified depth
                curr_eval = self.minimax(board, depth - 1, alpha, beta, True)[1]

                # unmake the move on the board
                board.undo_move()
                board.switch_turn()

                if curr_eval < min_eval:
                    min_eval = curr_eval
                    best_move = move

                beta = min(beta, curr_eval)

                if beta <= alpha:
                    break
            return best_move, min_eval

    @Profiler.profile
    def make_move(self, board: Board):
        """Choose (make a weighted choice) a move for the AI to make and make the move. Takes as input a board object"""
        start_pos, end_pos = self.minimax(board, self.max_depth, self.alpha, self.beta, True)[0]  # minimax
        board.move_piece(start_pos, end_pos)  # move using chess letter notation
        print(f"moving from {start_pos} to {end_pos}")
        print(board)


class Node:

    def __init__(self, board: Board, last_move, parent, first_move):
        # total = wins;  score = total / visits
        self.board = board
        self.move = last_move  # move from parent to node
        self.parent = parent  # parent node
        self.children = []  # list of child nodes
        self.total = 0
        self.visits = 0
        self.depth = 0
        self.samples = []
        self.first_move = first_move  # initial move

        if parent != None:
            self.depth = parent.depth + 1

    def is_leaf_node(self):
        return len(self.children) == 0

    def select_node(self):
        """Choose a node using the selection policy formula"""
        c = 4000
        lis = []
        for n in self.children:
            if n.visits == 0:
                s = float('inf')
            else:
                s = (n.total / n.visits) + (c * ((math.log(self.visits) / n.visits) ** 0.5))
            lis.append((n, s))

        v = max([e[1] for e in lis])
        best = [nd for nd, val in lis if val == v]
        child = random.choice(best)
        return child

    @staticmethod
    def temp_board_move(board, move):
        """Return a copy of the board after temporarily making a move"""
        board1 = copy.deepcopy(board)
        # make the move on the board
        piece1, piece2 = board1.get_piece_from_position(move[0]), board1.get_board()[move[1][1]][move[1][0]]
        pos1x, pos1y, pos2x, pos2y = move[0][0], move[0][1], move[1][0], move[1][1]
        board1.update_pieces(piece1, pos2x, pos2y)
        if isinstance(piece2, Piece):  # temporarily delete piece from dict if necessary
            board1.update_pieces(piece2, pos2x, pos2y, delete=True)
        board1.get_board()[pos1y][pos1x], board1.get_board()[pos2y][pos2x] = None, board1.get_board()[pos1y][
            pos1x]
        board1.update_move_count()
        board1.switch_turn()
        return board1

    def expand_node(self):
        if self.depth > 3:
            return self

        board = self.board
        if self.parent is None:  # is the root node
            for move in AI.format_legal_moves(board):
                board.move_piece(move[0], move[1])
                board.switch_turn()
                self.children.append(Node(board, move, self, move))
                board.undo_move()
                board.switch_turn()

        else:  # has a parent
            for move in AI.format_legal_moves(board):
                board.move_piece(move[0], move[1])
                board.switch_turn()
                self.children.append(Node(board, move, self, self.first_move))
                board.undo_move()
                board.switch_turn()

        return random.choice(self.children)  # random node

    def simulation(self, t, team):
        """Run a simulation, return a resulting score"""
        i = 0
        while (not self.board.is_game_over()) and (i < 20):
            # random move on the board
            moves = AI.format_legal_moves(self.board)
            move = random.choice(moves)

            # make move on the board
            self.board.move_piece(move[0], move[1])
            self.board.switch_turn()
            i += 1

        # TODO maybe use AI scoring to evaluate board instead of returning winner like this

        if i == 20:  # limit the depth of the simulation (going further doesn't really give any information)
            w = 0
        else:
            w = self.board.winner()
        w = AI.scoring(self.board, team)
        self.board._game_over = False

        for _ in range(i):
            self.board.undo_move()
            self.board.switch_turn()
        self.board._legal_moves = {}

        return w

    def backpropogate(self, result):
        self.visits += 1
        self.total += result
        self.samples.append(result)

        if self.parent != None:
            self.parent.backpropogate(result)


class MCTSAI(AI):

    def best_board(self, node):
        """Best action"""
        counter = {}
        for n in node.children:
            if len(n.samples) == 0:
                sample = 0
            else:
                sample = sum(n.samples) / len(n.samples)  # [sample] = [n.total / n.visits]
            counter[n.move] = sample
            print('d', n.move, sample, len(n.samples))
            #if n.move in counter.keys():
            #    counter[n.move] += [sample]
            #else:
            #    counter[n.move] = [sample]

        lis = counter.items()
        # print([(a, count[a], counter[a]) for a in counter.keys()])
        v = max(counter.values())
        best = [move for move, val in lis if val == v]
        return random.choice(best)

    def mcts(self, board: Board):
        start = time.time()
        root = Node(board, None, None, None)
        root.expand_node()
        i = 0
        while time.time() - start < 5:  # 0.9 seconds
            n = root
            while not n.is_leaf_node():
                n = n.select_node()
            if n.visits != 0:  # if leaf node not visited yet, then expand it
                n = n.expand_node()
            print('6', time.time() - start)
            result = n.simulation(start, self._team)
            print('7', time.time() - start)
            n.backpropogate(result)
            i += 1
        print(i)
        return self.best_board(root)

    @Profiler.profile
    def make_move(self, board: Board):
        """Choose (make a weighted choice) a move for the AI to make and make the move. Takes as input a board object"""
        start_pos, end_pos = self.mcts(board)
        board.move_piece(start_pos, end_pos)  # move using chess letter notation
        print(f"moving from {start_pos} to {end_pos}")
        print(board)
