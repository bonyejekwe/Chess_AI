
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

    def __init__(self, start_on_creation=False):
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
            self.start_game()

    def start_game(self):
        """Starts the game and draws the board"""
        result = self.run_game()  # Get the game result
        Profiler.report()
        print('The winner is: {} !!!'.format(result))  # Print the game result

    def initialize_board(self):
        """Draws the board to begin with and sets important instance variables"""
        pygame.display.set_caption("Chess Board")  # set caption

        self.display_board = pygame.Surface((self.width, self.height))  # Create the board surface
        self.display_board.fill(self.white)  # Fill it with white

        # Draw black squares on the board
        for x in range(0, 8):  # Loop through the x-axis
            for y in range(0, 8):  # Loop through the y-axis
                if (x + y) % 2 == 1:
                    pygame.draw.rect(self.display_board, self.black,
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def run_game(self):
        """Run game using num of AI's (1=player vs AI, 2=AI vs AI). Defaults to AI vs AI"""
        self.board = Board()  # Set the board

        # Get the side from the player
        self.side = input("Select side you would like to play on (1 for white, -1 for black): ")
        if self.side == "1" or self.side == "-1":
            self.side = int(self.side)
        else:
            raise InvalidTeamError(self.side)

        ai_team = -1 * self.side  # Set the ai's side

        # Get the desired AI type and define AI
        ai_types = {0: AI, 1: MinimaxAI, 2: MCTSAI}
        ai_type = input("Select AI to play against {0: AI, 1: MinimaxAI, 2: MCTSAI}: ")
        if ai_type == "0" or ai_type == "1" or ai_type == "2":
            ai_type = ai_types[int(ai_type)]
            ai = ai_type(ai_team)  # define the AI
        else:
            raise InvalidAIType(ai_type)

        self.board.start_game()  # Start the game
        self.initialize_board()  # Initialize the board
        game_winner = self.master_function(ai)  # Start the first turn
        return game_winner

    def master_function(self, game_ai):  # effectively defaults to no AI for game
        """The graphics master function"""
        game_exit = False  # Define the game exit variable
        game_display = pygame.display.set_mode((self.width, self.height))  # set display
        piece_to_move_chosen = False  # Set the variable for if a new move has been chosen
        chosen_piece = []  # Set the variable for the location of the chosen piece

        if self.side == -1:  # Check if the player's side is black, and if it is then have the AI make the first move
            pass

        while not game_exit:  # While the exit button has not been pressed
            if self.board.is_game_over():
                return self.board.winner()

            for event in pygame.event.get():  # Check the events
                if event.type == pygame.QUIT:  # If the event is quitting the application, then do so
                    game_exit = True

                # If the event is clicking the mouse, then get the position
                if event.type == pygame.MOUSEBUTTONUP and self.board.get_current_turn() == self.side:
                    pos = pygame.mouse.get_pos()  # Find the mouse position

                    # Find the chess coordinates of the chosen position
                    x, y = int(pos[0] / self.cell_size), 7 - int(pos[1] / self.cell_size)  # print(x, y)

                    # If this is the first piece we have chosen and it is a piece of our color
                    if (not piece_to_move_chosen) and isinstance(self.board.get_board()[y][x], Piece) and \
                            self.board.get_board()[y][x].get_color() == self.side:

                        # Change the background color of the cell
                        pygame.draw.rect(self.display_board, self.chosen_color, (
                        (x) * self.cell_size, (7 - y) * self.cell_size, self.cell_size, self.cell_size))

                        piece_to_move_chosen = True  # Change the variable to true
                        chosen_piece = [x, y]  # Save the location of the chosen piece

                    # Check if a piece has been chosen and the selected tile does not match the chosen piece tile
                    elif piece_to_move_chosen and (x != chosen_piece[0] or y != chosen_piece[1]):

                        try:  # Check that the move was valid using game code
                            self.board.move_piece(tuple(chosen_piece), (x, y))
                        except:  # This is far too general, but it is also not nearly finished
                            continue  # Exit out of current loop iteration

                        # Find out which color should be used
                        if (chosen_piece[0] + (7 - chosen_piece[1])) % 2 == 1:
                            overwrite_color = self.black
                        else:
                            overwrite_color = self.white

                        # Change the background color of the last location
                        pygame.draw.rect(self.display_board, overwrite_color, (
                        chosen_piece[0] * self.cell_size, (7 - chosen_piece[1]) * self.cell_size, self.cell_size,
                        self.cell_size))

                        piece_to_move_chosen = False  # set the piece_to_move_chosen to false
                        self.board.switch_turn()  # Change the current turn

                        if self.board.is_game_over():  # Check if the game is over
                            return self.board.winner()

                    elif piece_to_move_chosen and (x == chosen_piece[0] and y == chosen_piece[1]):
                        # Find out which color should be used
                        if (chosen_piece[0] + (7 - chosen_piece[1])) % 2 == 1:
                            overwrite_color = self.black
                        else:
                            overwrite_color = self.white

                        # Change the background color of the last location
                        pygame.draw.rect(self.display_board, overwrite_color, (
                        chosen_piece[0] * self.cell_size, (7 - chosen_piece[1]) * self.cell_size, self.cell_size,
                        self.cell_size))

                        piece_to_move_chosen = False  # Reset the chosen piece variable

            game_display.blit(self.display_board, self.display_board.get_rect())  # Fill the display with the board
            self.draw_pieces(game_display)  # Draw the pieces on the board
            pygame.display.update()  # Update the display

            if self.board.get_current_turn() == -1 * self.side:  # If its the computer's turn
                if self.board.is_game_over():  # Check if the game is over
                    return self.board.winner()

                if self.board.is_in_check(self.board.get_current_turn()):  # Check if a player is in check
                    for _ in range(10):
                        print(f'{self.board.get_current_turn()} is in check!!!')

                game_ai.all_legal_moves(self.board)  # Make the AI move
                game_ai.make_move(self.board)

                if self.board.is_game_over():  # Check if the game is over
                    return self.board.winner()

                if self.board.is_in_check(self.board.get_current_turn()):  # Check if a player is in check
                    for _ in range(10):
                        print(f'{self.board.get_current_turn()} is in check!!!')

                self.board.switch_turn()  # Switch the turn

        pygame.quit()  # Quit pygame

    def draw_pieces(self, game_display):
        """Blitzes the pieces onto the board"""
        brd = self.board.get_board()  # Get the board

        for y in range(len(brd)):  # Iterating over rows\
            for x in range(len(brd[y])):  # Iterating over the columns
                if isinstance(brd[x][y], Piece):  # Check that the element is a piece
                    piece_type = str(brd[x][y])[0]  # Find the piece type
                    piece_color = brd[x][y].get_color()  # 1 is white and -1 is black

                    # Draw the respective piece
                    if piece_color == 1:
                        game_display.blit(self.white_pieces[piece_type],
                                         (self.cell_size * y, self.cell_size * (7 - x)))

                    elif piece_color == -1:
                        game_display.blit(self.black_pieces[piece_type],
                                         (self.cell_size * y, self.cell_size * (7 - x)))


def main():
    PlayGame(True)


if __name__ == "__main__":
    main()
