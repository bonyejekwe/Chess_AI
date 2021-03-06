
# AI.py: our chess AI

#  -"basic" just favors capturing pieces of equal or lesser value, and favors not moving the king (need add more)
#  -"medium" is minimax implemented (w/ alpha beta pruning), using AI scoring criteria

import time
import math
import random
from pieces import *
from board import Board, NoKingError, InvalidBoardMoveError
from profiler import Profiler


class AI:

    def __init__(self, color: int):
        self._team = color
        self.zob_hashing = {}
        self.transpositions = 0

    @Profiler.profile
    def scoring(self, board: Board, color: int) -> int:
        """Generalized scoring system: score is positive if white is winning and negative if black
         is winning, the magnitude shows by how much one side is winning
        :param board: The board (represented as an 8x8 list of lists containing piece objects)
        :param color: The team of the side in question
        :return: A generalized score (int) for the difference in total piece worth for each side."""
        zob = board.get_zobrist_hash()
        if zob in self.zob_hashing.keys():
            self.transpositions += 1
            return self.zob_hashing[zob]

        try:
            if board.checkmate():
                # large negative if AI team in checkmate, positive otherwise
                return -999999 * board.get_current_turn() * color

        except NoKingError:
            print(board)
            pass

        scores = []  # [AI score, other team score]
        num_moves = board.get_current_move_count()
        for team in [1, -1]:
            consider = board.get_pieces_left(color * team)  # pieces left for AI, then pieces left for other team

            worth_weights = []  # initial weighting: get the difference in worth for each team
            constant_dev = []  # development of pieces that should stay the same throughout the game
            diminishing_dev = []  # development of pieces that should become less important as game goes on
            piece_development = []  # general piece development: increase weight if pieces have many options to move

            for p in consider:
                x, y = consider[p]
                if isinstance(p, Pawn) or isinstance(p, Knight):  # diminish importance as game goes on
                    diminishing_dev.append(p.eval[y][x])
                else:
                    constant_dev.append(p.eval[y][x])

                if not isinstance(p, Pawn):
                    piece_development.append(len(p.legal_moves()) * p.get_worth() / 100)
                worth_weights.append(p.get_worth())

            score = sum(worth_weights)
            score += sum(diminishing_dev) + (sum(constant_dev))
            # score += (sum(diminishing_dev) / num_moves) + (sum(constant_dev))
            # score += 15 * sum(piece_development)
            scores.append(score)

        score = scores[0] - scores[1]
        self.zob_hashing[zob] = score
        return score  # AI score - other score

    def get_team(self):
        """:return: The team the AI is"""
        return self._team

    @staticmethod
    def format_legal_moves(board: Board):
        """Retrieve the legal moves for the AI. Return as a list of tuples of tuples. Takes as input a board object."""
        all_moves = []
        d = board.legal_moves()  # key = piece position : values = list of possible next moves (tuples)
        for pos in d:
            for val in d[pos]:
                all_moves.append((pos, val))  # ((x1, y1), (x2, y2)): move: p1 -> p2
        return all_moves

    @staticmethod
    def num_pos_to_letter_pos(position: tuple) -> tuple:
        """Converts a position like (0,0) to (A,1)
        :param position: Position you would like convert
        :return: A tuple with chess letter notation as position"""
        return chr(position[0] + 65), position[1] + 1  # a tuple

    @Profiler.profile
    def make_move(self, board: Board):
        """Choose (make a weighted choice) a move for the AI to make and make the move. Takes as input a board object"""
        moves_dict = {m: 1 for m in self.format_legal_moves(board)}
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
        self.max_depth = 4

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
            return None, self.scoring(board, self._team)

        moves = self.format_legal_moves(board)[::-1]
        best_move = moves[0]

        if maximizing_player:
            max_eval = -1 * float('inf')
            for move in moves:
                board.move_piece(move[0], move[1], check=False)  # make the move on the board

                # make a recursive call to minimax to find the best evaluation at a specified depth
                curr_eval = self.minimax(board, depth - 1, alpha, beta, False)[1]

                board.undo_move()  # unmake the move on the board

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
                board.move_piece(move[0], move[1], check=False)  # make the move on the board

                # make a recursive call to minimax to find the best evaluation at a specified depth
                curr_eval = self.minimax(board, depth - 1, alpha, beta, True)[1]

                board.undo_move()  # unmake the move on the board

                if curr_eval < min_eval:
                    min_eval = curr_eval
                    best_move = move

                beta = min(beta, curr_eval)

                if beta <= alpha:
                    break
            return best_move, min_eval

    @Profiler.profile
    def make_move(self, board: Board):
        """Choose a move for the AI to make and make the move. Takes as input a board object"""
        start_pos, end_pos = self.minimax(board, self.max_depth, self.alpha, self.beta, True)[0]  # minimax
        print('t', self.transpositions)
        print('h', len(self.zob_hashing))
        board.move_piece(start_pos, end_pos)  # move piece on the board
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

        if parent is not None:
            self.depth = parent.depth + 1

    def is_leaf_node(self):
        return len(self.children) == 0

    def select_node(self):
        """Choose a node using the selection policy formula"""
        c = 400
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

    def expand_node(self):
        if self.depth > 2:
            return self

        board = self.board
        for move in AI.format_legal_moves(board):
            board.move_piece(move[0], move[1])
            if self.parent is None:  # is the root node
                self.children.append(Node(board, move, self, move))
            else:
                self.children.append(Node(board, move, self, self.first_move))
            board.undo_move()

        return random.choice(self.children)  # random node

    def simulation(self, t, team):
        """Run a simulation, return a resulting score"""
        i = 0  # limit the depth of the simulation (going further doesn't really give any information)
        while (not self.board.is_game_over()) and (i < 5):
            # random move on the board
            moves = AI.format_legal_moves(self.board)
            move = random.choice(moves)

            # make move on the board
            self.board.move_piece(move[0], move[1])
            i += 1

        w = MCTSAI(1).scoring(self.board, team)

        for _ in range(i):
            self.board.undo_move()
        self.board._legal_moves = {}

        return w

    def backpropogate(self, result):
        self.visits += 1
        self.total += result
        self.samples.append(result)

        if self.parent is not None:
            self.parent.backpropogate(result)


class MCTSAI(AI):

    @staticmethod
    def best_board(node):
        """Best action"""
        counter = {}
        s = 0
        for n in node.children:
            if len(n.samples) == 0:
                sample = 0
            else:
                sample = sum(n.samples) / len(n.samples)  # [sample] = [n.total / n.visits]
            counter[n.move] = sample
            print('d', n.move, sample, len(n.samples))
            s += len(n.samples)
        print('s', s)

        lis = counter.items()
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
            #print('4', time.time() - start)
            while not n.is_leaf_node():
                n = n.select_node()
            #print('5', time.time() - start)
            if n.visits != 0:  # if leaf node not visited yet, then expand it
                n = n.expand_node()
            #print('6', time.time() - start)
            result = n.simulation(start, self._team)
            #print('7', time.time() - start)
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


class IterativeDeepeningAI(MinimaxAI):

    def __init__(self, color: int):
        super().__init__(color)
        self.max_depth = 4
        self.move_ordering = {}

    def ids(self, board: Board, depth: int):
        """Run iterative deepening search on a board to a specified depth"""
        self.move_ordering = {}
        print('starting iterations')

        for i in range(1, depth):  # [1, 2, ... depth]
            self.minimax(board, i, self.alpha, self.beta, True)
            print('iter depth', i)
            print('l', len(self.move_ordering))
            print(self.move_ordering[board.get_zobrist_hash()][::-1][:5])

        result = self.minimax(board, depth, self.alpha, self.beta, True)
        print('iter depth', depth)
        print('l', len(self.move_ordering))
        print(self.move_ordering[board.get_zobrist_hash()][::-1])
        return result

    @Profiler.profile
    def minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool):
        """Implement minimax algorithm: the best move for the maximizing color looking ahead depth moves on the board
        :param board: The current board being evaluated
        :param depth: The current depth being evaluated
        :param alpha: value for alpha
        :param beta: value for beta
        :param maximizing_player: bool representing whether the AI's team is maximizing their score at the current depth
        :return: A tuple with best move and best evaluation"""
        ordered_moves = []
        zob = board.get_zobrist_hash()

        if depth == 0 or board.is_game_over():  # base case: depth = 0
            return None, self.scoring(board, self._team)

        if zob in self.move_ordering.keys():
            moves = self.move_ordering[zob]
        else:
            moves = self.format_legal_moves(board)

        best_move = moves[0]

        if maximizing_player:
            max_eval = -1 * float('inf')
            while moves:  # while moves != []
                move = moves.pop()

                # make the move on the board
                board.move_piece(move[0], move[1], check=False)

                # make a recursive call to minimax to find the best evaluation at a specified depth
                curr_eval = self.minimax(board, depth - 1, alpha, beta, False)[1]
                ordered_moves.append((move, curr_eval))

                # unmake the move on the board
                board.undo_move()

                if curr_eval > max_eval:
                    max_eval = curr_eval
                    best_move = move

                alpha = max(alpha, curr_eval)

                if beta <= alpha:
                    break

            ordered_moves = sorted(ordered_moves, key=lambda x: x[1])
            self.move_ordering[zob] = moves + [i[0] for i in ordered_moves]  # worst to best
            return best_move, max_eval

        else:
            min_eval = float('inf')
            while moves:  # moves != []:
                move = moves.pop()
                # make the move on the board
                board.move_piece(move[0], move[1], check=False)

                # make a recursive call to minimax to find the best evaluation at a specified depth
                curr_eval = self.minimax(board, depth - 1, alpha, beta, True)[1]
                ordered_moves.append((move, curr_eval))

                # unmake the move on the board
                board.undo_move()

                if curr_eval < min_eval:
                    min_eval = curr_eval
                    best_move = move

                beta = min(beta, curr_eval)

                if beta <= alpha:
                    break

            ordered_moves = sorted(ordered_moves, key=lambda x: x[1])
            self.move_ordering[zob] = moves + [i[0] for i in ordered_moves]  # worst to best
            return best_move, min_eval

    @Profiler.profile
    def make_move(self, board: Board):
        """Choose (make a weighted choice) a move for the AI to make and make the move. Takes as input a board object"""
        # start_pos, end_pos = self.ids(board, self.max_depth, self.alpha, self.beta, True, None)
        start_pos, end_pos = self.ids(board, self.max_depth)[0]  # minimax
        board.move_piece(start_pos, end_pos)  # move using chess letter notation
        print(f"moving from {start_pos} to {end_pos}")
        print(board)
