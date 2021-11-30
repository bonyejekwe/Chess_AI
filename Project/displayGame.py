
# TODO README!!!!
#  Currently each game is capped to take less than 200 moves and any game taking longer is listed as a timeout.
#  NOTE: this can be changed, but game code for performance.py: 1= white checkmate win, -1=black checkmate win, 2=white
#  stalemated (black can't move), -2=black stalemated (white can't move), 0=draw?, -5=timeout (over 200 moves)

from board import Board
from AI import AI

import pygame

## Function used for performance testing
def run_game(num=2, mode1="random", mode2="random"):
    """Run game using num of AI's (1=player vs AI, 2=AI vs AI). Defaults to AI vs AI"""
    game = Board()
    if num == 1:  # player against ai
        side = int(input("Select side you would like to play on (1 for white, -1 for black): "))
        ai_team = -1 * side
        ai = AI(ai_team, mode1)
        ai2 = False
    else:
        ai = AI(1, mode1)
        ai2 = AI(-1, mode2)
        
    game.start_game()
    
    game_winner = turn(game, ai, ai2)  # run the game
    print("the winner is...", game_winner)
    return game_winner


# Class for playing the game
class playGame :
    
    
    def __init__(self, start_on_creation = False, AI_mode='medium'):
        ''' Initializes the variable, and starts the game automatically if desired'''
            
        # Set the constant variables ( stored as instance variables in case they become changable in the future)
        self.white, self.black = (240, 217, 181), (181, 136, 99)
        
        # Set the chosen color
        self.chosen_color = (54, 173, 74)
        
        # Define the width, height, and cell size
        self.width, self.height = 800, 800
        # Define the cell size
        self.cell_size = self.width / 8.0
        
        if start_on_creation == True:
            self.start_game(AI_mode)
            
    
    def start_game(self, AI_mode='medium'):
        ''' Starts the game and draws the board '''
        
        # Get the game result
        result = self.run_game(AI_mode)
        
        # Print the game result
        print('The winner is: {} !!!'.format(result))

    def initialize_board(self):
        ''' Draws the board to begin with and sets important instance variables'''
        # set caption
        pygame.display.set_caption("Chess Board")

        # Create the board surface
        self.board = pygame.Surface((self.width, self.height))
        # Fill it with white
        self.board.fill(self.white)
        
        # Draw black squares on the board
        # Loop through the x-axis
        for x in range(0, 8):
            # Loop through the y-axis
            for y in range(0, 8):
                # If the 
                if (x + y) % 2 == 1:
                    pygame.draw.rect(self.board, self.black, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
    
    def run_game(self, mode = "medium"):
        """Run game using num of AI's (1=player vs AI, 2=AI vs AI). Defaults to AI vs AI"""
        # Set the 
        self.game = Board()
    
        # Get the side from the player
        #side = int(input("Select side you would like to play on (1 for white, -1 for black): "))
        side = 1
        # Set the ai's side
        ai_team = -1 * side
        # Define the ai
        ai = AI(ai_team, mode)
        # Set ai2 variable to false
        ai2 = False

        # Start the game
        self.game.start_game()
    
        # Initialize the board
        self.initialize_board()
        
        # Start the first turn
        game_winner = self.turn(self.game, ai, ai2)  # run the game
        
        return game_winner



    def turn(self, game, ai_game, ai_game2=False):  # effectively defaults to no AI for game
        timed_out = -5
        while game.is_game_over() is False and game.get_current_move_count() < 200:
            move(game, ai_game, ai_game2)
            game.switch_turn()
            print(f"Turn #: {game.get_current_move_count()}...")
            # print(f"captured: {[str(p) for p in game.get_captured()]}")
            if game.is_game_over():
                return game.winner()
            else:
                print('timed out')
                return timed_out


def move(game: Board, game_ai: AI, game_ai2=False):
    if game.get_current_turn() == 1:
        print("White's turn.")
        mv_string = "Location of piece, ie A2: "
        ds_string = "Desired position, ie A3: "
    else:
        print("Black's turn.")
        mv_string = "Location of piece, ie A7: "
        ds_string = "Desired position, ie A6: "

    if game.is_in_check(game.get_current_turn()):
        for _ in range(10):
            print(f'{game.get_current_turn()} is in check!!!')

    if game_ai.get_team() == game.get_current_turn():  # AI's turn
        game_ai.all_legal_moves(game)
        game_ai.make_move(game)
    elif game_ai2:
        if game_ai2.get_team() == game.get_current_turn():  # AI's turn
            game_ai2.all_legal_moves(game)
            game_ai2.make_move(game)
    else:
        # take positions from input
        moving_piece = list(input(mv_string))
        moving_piece[0] = moving_piece[0].upper()
        moving_piece[1] = int(moving_piece[1])
        moving_piece = tuple(moving_piece)
        
        
        desired_position = list(input(ds_string))
        desired_position[0] = desired_position[0].upper()
        desired_position[1] = int(desired_position[1])
        desired_position = tuple(desired_position)
        # need error check tuples, a-h, 1-8, len = 2, custom exceptions
        try:
            game.move_piece(moving_piece, desired_position)
            print("move successful")
        except:  # This is far too general, but it is also not nearly finished
            print(game.__repr__())
            print('Redo move.')
            move(game, game_ai, game_ai2)


def main():
    playGame(True)

if __name__ == "__main__":
    main()
