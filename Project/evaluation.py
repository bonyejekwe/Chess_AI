
from all_moves import all_positions
# index by team, ypos, xpos  (board is flipped over x axis,
white_pawn_dev = [[-5, -5, -5, -5, -5, -5, -5, -5],  # 1
                  [0, 0, 0, 0, 0, 0, 0, 0],          # 2
                  [5, 5, 5, 5, 5, 5, 5, 5],          # 3
                  [10, 10, 10, 10, 10, 10, 10, 10],  # 4
                  [15, 15, 15, 15, 15, 15, 15, 15],  # 5
                  [20, 20, 20, 20, 20, 20, 20, 20],  # 6
                  [25, 25, 25, 25, 25, 25, 25, 25],  # 7
                  [30, 30, 30, 30, 30, 30, 30, 30]]  # 8

black_pawn_dev = [[30, 30, 30, 30, 30, 30, 30, 30],
                  [25, 25, 25, 25, 25, 25, 25, 25],
                  [20, 20, 20, 20, 20, 20, 20, 20],
                  [15, 15, 15, 15, 15, 15, 15, 15],
                  [10, 10, 10, 10, 10, 10, 10, 10],
                  [5, 5, 5, 5, 5, 5, 5, 5],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [-5, -5, -5, -5, -5, -5, -5, -5]]

white_knight_dev = [[40, 40, 40, 40, 40, 40, 40, 40],
                    [60, 60, 60, 60, 60, 60, 60, 60],
                    [80, 80, 80, 80, 80, 80, 80, 80],
                    [100, 100, 100, 100, 100, 100, 100, 100],
                    [80, 80, 80, 80, 80, 80, 80, 80],
                    [60, 60, 60, 60, 60, 60, 60, 60],
                    [40, 40, 40, 40, 40, 40, 40, 40],
                    [20, 20, 20, 20, 20, 20, 20, 20]]

black_knight_dev = [[40, 40, 40, 40, 40, 40, 40, 40],
                    [60, 60, 60, 60, 60, 60, 60, 60],
                    [80, 80, 80, 80, 80, 80, 80, 80],
                    [100, 100, 100, 100, 100, 100, 100, 100],
                    [80, 80, 80, 80, 80, 80, 80, 80],
                    [60, 60, 60, 60, 60, 60, 60, 60],
                    [40, 40, 40, 40, 40, 40, 40, 40],
                    [20, 20, 20, 20, 20, 20, 20, 20]]

white_king_dev = [[80, 80, 80, 80, 80, 80, 80, 80],
                  [70, 70, 70, 70, 70, 70, 70, 70],
                  [60, 60, 60, 60, 60, 60, 60, 60],
                  [50, 50, 50, 50, 50, 50, 50, 50],
                  [40, 40, 40, 40, 40, 40, 40, 40],
                  [30, 30, 30, 30, 30, 30, 30, 30],
                  [20, 20, 20, 20, 20, 20, 20, 20],
                  [10, 10, 10, 10, 10, 10, 10, 10]]

black_king_dev = [[10, 10, 10, 10, 10, 10, 10, 10],
                  [20, 20, 20, 20, 20, 20, 20, 20],
                  [30, 30, 30, 30, 30, 30, 30, 30],
                  [40, 40, 40, 40, 40, 40, 40, 40],
                  [50, 50, 50, 50, 50, 50, 50, 50],
                  [60, 60, 60, 60, 60, 60, 60, 60],
                  [70, 70, 70, 70, 70, 70, 70, 70],
                  [80, 80, 80, 80, 80, 80, 80, 80]]

white_rook_dev = [[0 for _ in range(8)] for _ in range(8)]
black_rook_dev = [[0 for _ in range(8)] for _ in range(8)]
white_queen_dev = [[0 for _ in range(8)] for _ in range(8)]
black_queen_dev = [[0 for _ in range(8)] for _ in range(8)]
white_bishop_dev = [[0 for _ in range(8)] for _ in range(8)]
black_bishop_dev = [[0 for _ in range(8)] for _ in range(8)]

def evaluating(team):
    d = {1: 0, -1: 7}
    m = [[None for _ in range(8)] for _ in range(8)]
    for x, y in all_positions:
        # m[y][x] = (5 * y * team) + (12.5 - (17.5 * team))  # pawn
        m[y][x] = 80 - (10 * abs(y - d[team]))
    for row in m:
        print(row)


#evaluating(1)
#print('')
#evaluating(-1)

# pawn development: increase score if pawns are moving up the board
# knight development: increase score if pawns are moving up the board
# king development: increase score if king is not moving up the board
