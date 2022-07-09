
# displayGame.py: a graphical user interface (GUI) for our chess AI

from board import Board
from AI import *
from pieces import *
import pygame


class InvalidTeamError(Exception):
    def __init__(self, team):
        super().__init__(f"Invalid Team: {team} is not a valid team. Must be either 1 or -1")


class InvalidAIType(Exception):
    def __init__(self, ty):
        super().__init__(f"Invalid AI Type: {ty} is not a valid team. Must be either 1, 2, 3, or 4")


class PlayGame:

    def __init__(self, start_on_creation=False, ai_mode='medium'):
        """Initializes the variable, and starts the game automatically if desired"""

        # Set the constant variables ( stored as instance variables in case they become changeable in the future)
        self.white, self.black = (240, 217, 181), (181, 136, 99)
        self.chosen_color = (54, 173, 74)  # Set the chosen color
        self.width, self.height = 800, 800  # Define the width, height, and cell size
        self.cell_size = self.width / 8.0  # Define the cell size
        self.pos_pieces = ['K', 'Q', 'B', 'R', 'N', 'P']  # Define the possible pieces

        # Get the piece images
        self.white_pieces = {
            self.pos_pieces[i]: pygame.transform.scale(pygame.image.load(r'Piece Images/{}/{}.png'.format(
                'white', self.pos_pieces[i])), (100, 100)) for i in range(len(self.pos_pieces))}

        self.black_pieces = {
            self.pos_pieces[i]: pygame.transform.scale(pygame.image.load(r'Piece Images/{}/{}.png'.format(
                'black', self.pos_pieces[i])), (100, 100)) for i in range(len(self.pos_pieces))}

        if start_on_creation:
            self.start_game(ai_mode)

    def start_game(self, AI_mode='medium'):
        """Starts the game and draws the board"""
        # Get the game result
        result = self.run_game(AI_mode)
        Profiler.report()
        # Print the game result
        print('The winner is: {} !!!'.format(result))

    def initialize_board(self):
        """Draws the board to begin with and sets important instance variables"""
        pygame.display.set_caption("Chess Board")  # set caption

        self.board = pygame.Surface((self.width, self.height))  # Create the board surface
        self.board.fill(self.white)  # Fill it with white

        # Draw black squares on the board
        for x in range(0, 8):  # Loop through the x-axis
            for y in range(0, 8):  # Loop through the y-axis
                if (x + y) % 2 == 1:
                    pygame.draw.rect(self.board, self.black,
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def run_game(self, mode="medium"):
        """Run game using num of AI's (1=player vs AI, 2=AI vs AI). Defaults to AI vs AI"""
        self.game = Board()  # Set the board

        # Get the side from the player
        self.side = input("Select side you would like to play on (1 for white, -1 for black): ")
        if self.side == "1" or self.side == "-1":
            self.side = int(self.side)
        else:
            raise InvalidTeamError(self.side)

        # Set the ai's side
        ai_team = -1 * self.side

        # Get the desired AI type and define AI
        ai_types = {0: AI, 1: MinimaxAI, 2: MCTSAI}
        ai_type = input("Select AI to play against {0: AI, 1: MinimaxAI, 2: MCTSAI}: ")
        if ai_type == "0" or ai_type == "1" or ai_type == "2" or ai_type == "3":
            ai_type = ai_types[int(ai_type)]
            ai = ai_type(ai_team, "medium")  # define the AI
        else:
            raise InvalidAIType(ai_type)

        self.game.start_game()  # Start the game
        self.initialize_board()  # Initialize the board
        game_winner = self.master_function(ai)  # Start the first turn
        return game_winner

    def master_function(self, game_ai):  # effectively defaults to no AI for game
        """The graphics master function"""
        # Define a dictionary of letters to map
        letters_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

        # Define the game exit variable
        game_exit = False

        # set display
        gameDisplay = pygame.display.set_mode((self.width, self.height))

        # Set the variable for if a new move has been chosen
        piece_to_move_chosen = False

        # Set the variable for the location of the chosen piece
        chosen_piece = []

        # Check if the player's side is black, and if it is then have the AI make the first move
        if self.side == -1:
            pass

        # While the exit button has not been pressed
        while not game_exit:

            if self.game.is_game_over():
                return self.game.winner()

            # Check the events
            for event in pygame.event.get():
                # If the event is quitting the application, then do so
                if event.type == pygame.QUIT:
                    game_exit = True

                # If the event is clicking the mouse, then get the position
                if event.type == pygame.MOUSEBUTTONUP and self.game.get_current_turn() == self.side:
                    # Find the mouse position
                    pos = pygame.mouse.get_pos()

                    # Find the chess coordinates of the chosen position
                    x, y = int(pos[0] / self.cell_size), 7 - int(pos[1] / self.cell_size)

                    # print(x, y)

                    # If this is the first piece we have chosen and it is a piece of our color
                    if (not piece_to_move_chosen) and isinstance(self.game.get_board()[y][x], Piece) and \
                            self.game.get_board()[y][x].get_color() == self.side:

                        # Change the background color of the cell
                        pygame.draw.rect(self.board, self.chosen_color, (
                        (x) * self.cell_size, (7 - y) * self.cell_size, self.cell_size, self.cell_size))

                        # Change the variable to true
                        piece_to_move_chosen = True

                        # Save the location of the chosen piece
                        chosen_piece = [x, y]

                    # Check if a piece has been chosen and the selected tile does not match the chosen piece tile
                    elif piece_to_move_chosen and (x != chosen_piece[0] or y != chosen_piece[1]):

                        # Check that the move was valid using game code
                        try:
                            self.game.move_piece(tuple([letters_map[chosen_piece[0]], 1 + chosen_piece[1]]),
                                                 tuple([letters_map[x], 1 + y]))

                        except:  # This is far too general, but it is also not nearly finished
                            # Exit out of current loop iteration
                            continue

                        # Find out which color should be used
                        if (chosen_piece[0] + (7 - chosen_piece[1])) % 2 == 1:
                            overwrite_color = self.black
                        else:
                            overwrite_color = self.white

                        # Change the background color of the last location
                        pygame.draw.rect(self.board, overwrite_color, (
                        chosen_piece[0] * self.cell_size, (7 - chosen_piece[1]) * self.cell_size, self.cell_size,
                        self.cell_size))

                        # set the piece_to_move_chosen to false
                        piece_to_move_chosen = False

                        # Change the current turn
                        self.game.switch_turn()

                        # Check if the game is over
                        if self.game.is_game_over():
                            return self.game.winner()

                    elif piece_to_move_chosen and (x == chosen_piece[0] and y == chosen_piece[1]):
                        # Find out which color should be used
                        if (chosen_piece[0] + (7 - chosen_piece[1])) % 2 == 1:
                            overwrite_color = self.black
                        else:
                            overwrite_color = self.white

                        # Change the background color of the last location
                        pygame.draw.rect(self.board, overwrite_color, (
                        chosen_piece[0] * self.cell_size, (7 - chosen_piece[1]) * self.cell_size, self.cell_size,
                        self.cell_size))

                        # Reset the chosen piece variable
                        piece_to_move_chosen = False

            # Fill the display with the board
            gameDisplay.blit(self.board, self.board.get_rect())

            # Draw the pieces on the board
            self.draw_pieces(gameDisplay)

            # Update the display
            pygame.display.update()

            # If its the computer's turn
            if self.game.get_current_turn() == -1 * self.side:
                # Check if the game is over
                if self.game.is_game_over():
                    return self.game.winner()

                # Check if a player is in check
                if self.game.is_in_check(self.game.get_current_turn()):
                    for _ in range(10):
                        print(f'{self.game.get_current_turn()} is in check!!!')

                # Make the AI move
                game_ai.all_legal_moves(self.game)
                game_ai.make_move(self.game)

                # Check if teh game is over
                if self.game.is_game_over():
                    return self.game.winner()

                # Check if a player is in check
                if self.game.is_in_check(self.game.get_current_turn()):
                    for _ in range(10):
                        print(f'{self.game.get_current_turn()} is in check!!!')

                # Switch the turn
                self.game.switch_turn()

        # Quit pygame
        pygame.quit()

    def draw_pieces(self, gameDisplay):
        """Blitzes the pieces onto the board"""
        # Get the board
        brd = self.game.get_board()

        # Iterating over rows
        for y in range(len(brd)):

            # Iterating over the columns
            for x in range(len(brd[y])):

                # Check that the element is a piece
                if isinstance(brd[x][y], Piece):

                    # Find the piece type
                    piece_type = str(brd[x][y])[0]

                    # 1 is white and -1 is black
                    piece_color = brd[x][y].get_color()

                    # Draw the respective piece
                    if piece_color == 1:
                        gameDisplay.blit(self.white_pieces[piece_type],
                                         (self.cell_size * y, self.cell_size * (7 - x)))

                    elif piece_color == -1:
                        gameDisplay.blit(self.black_pieces[piece_type],
                                         (self.cell_size * y, self.cell_size * (7 - x)))


def main():
    PlayGame(True)


if __name__ == "__main__":
    main()
