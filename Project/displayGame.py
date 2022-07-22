# displayGame.py: a graphical user interface (GUI) for our chess AI

import pygame
from AI import *
from pieces import *
from all_moves import all_positions


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
        self.cell_size = 100  # Define the cell size (self.width / 8.0)
        self.pos_pieces = ['K', 'Q', 'B', 'R', 'N', 'P']  # Define the possible pieces

        # Get the piece images
        self.white_pieces = {p: pygame.transform.scale(pygame.image.load(r'Piece Images/{}/{}.png'.format(
            'white', p)), (100, 100)) for p in self.pos_pieces}

        self.black_pieces = {p: pygame.transform.scale(pygame.image.load(r'Piece Images/{}/{}.png'.format(
            'black', p)), (100, 100)) for p in self.pos_pieces}

        self.display_board = pygame.Surface((self.width, self.height))  # Create the board display surface
        self.board = Board()  # Create the board

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
        self.display_board.fill(self.white)  # Fill board with white squares

        # Draw black squares on the board
        for x, y in all_positions:  # Loop through all_positions
            if (x + y) % 2 == 1:
                rect_dim = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.display_board, self.black, rect_dim)

    def run_game(self):
        """Run game using num of AI's (1=player vs AI, 2=AI vs AI). Defaults to AI vs AI"""
        # Get the side from the player
        side = input("Select side you would like to play on (1 for white, -1 for black): ")
        if side == "1" or side == "-1":
            side = int(side)
        else:
            raise InvalidTeamError(side)

        ai_team = -1 * side  # Set the ai's side

        # Get the desired AI type and define AI
        ai_types = {0: AI, 1: MinimaxAI, 2: MCTSAI, 3: IterativeDeepeningAI}
        ai_type = input("Select AI to play against {0: AI, 1: MinimaxAI, 2: MCTSAI, 3: IterativeDeepeningAI}: ")
        if ai_type == "0" or ai_type == "1" or ai_type == "2" or ai_type == "3":
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

        side = -1 * game_ai.get_team()  # side is the player's team
        if side == -1:  # Check if the player's side is black, and if it is then have the AI make the first move
            pass

        while not game_exit:  # While the exit button has not been pressed
            if self.board.is_game_over():
                return self.board.winner()

            for event in pygame.event.get():  # Check the events
                if event.type == pygame.QUIT:  # If the event is quitting the application, then do so
                    game_exit = True

                # If the event is clicking the mouse, then get the position
                if event.type == pygame.MOUSEBUTTONUP and self.board.get_current_turn() == side:
                    pos = pygame.mouse.get_pos()  # Find the mouse position

                    # Find the chess coordinates of the chosen position
                    x, y = int(pos[0] / self.cell_size), 7 - int(pos[1] / self.cell_size)

                    if piece_to_move_chosen:  # piece has already been selected
                        if x != chosen_piece[0] or y != chosen_piece[1]:  # new piece chosen
                            try:  # Check that the move was valid
                                self.board.move_piece(tuple(chosen_piece), (x, y))
                            except InvalidBoardMoveError:
                                continue  # Exit out of current loop iteration

                            # Find out which color should be used
                            if (chosen_piece[0] + (7 - chosen_piece[1])) % 2 == 1:
                                overwrite_color = self.black
                            else:
                                overwrite_color = self.white

                            # Change the background color of the last location
                            rect_dim = (chosen_piece[0] * self.cell_size, (7 - chosen_piece[1]) * self.cell_size,
                                        self.cell_size, self.cell_size)
                            pygame.draw.rect(self.display_board, overwrite_color, rect_dim)

                            piece_to_move_chosen = False  # set the piece_to_move_chosen to false

                            if self.board.is_game_over():  # Check if the game is over
                                return self.board.winner()

                        else:  # x == chosen_piece[0] and y == chosen_piece[1]
                            # Find out which color should be used
                            if (chosen_piece[0] + (7 - chosen_piece[1])) % 2 == 1:
                                overwrite_color = self.black
                            else:
                                overwrite_color = self.white

                            # Change the background color of the last location
                            rect_dim = (chosen_piece[0] * self.cell_size, (7 - chosen_piece[1]) * self.cell_size,
                                        self.cell_size, self.cell_size)
                            pygame.draw.rect(self.display_board, overwrite_color, rect_dim)

                            piece_to_move_chosen = False  # Reset the chosen piece variable

                    else:  # no piece chosen before
                        if isinstance(self.board.get_board()[y][x], Piece) and self.board.get_board()[y][x].get_color() == side:
                            # Change the background color of the cell to green
                            rect_dim = (x * self.cell_size, (7 - y) * self.cell_size, self.cell_size, self.cell_size)
                            pygame.draw.rect(self.display_board, self.chosen_color, rect_dim)

                            piece_to_move_chosen = True  # Change the variable to true
                            chosen_piece = [x, y]  # Save the location of the chosen piece

            game_display.blit(self.display_board, self.display_board.get_rect())  # Fill the display with the board
            self.draw_pieces(game_display)  # Draw the pieces on the board
            pygame.display.update()  # Update the display

            if self.board.get_current_turn() == -1 * side:  # If its the computer's turn
                game_ai.make_move(self.board)  # Make the AI move

        pygame.quit()  # Quit pygame

    def draw_pieces(self, game_display):
        """Blitzes the pieces onto the board"""
        brd = self.board.get_board()  # Get the board

        for x, y in all_positions:  # iterate over all_positions
            if isinstance(brd[x][y], Piece):  # Check that the element is a piece
                piece_type = str(brd[x][y]).upper()  # Find the piece type
                piece_color = brd[x][y].get_color()  # 1 is white and -1 is black

                if piece_color == 1:  # draw the white pieces
                    game_display.blit(self.white_pieces[piece_type], (self.cell_size * y, self.cell_size * (7 - x)))
                elif piece_color == -1:  # draw the black pieces
                    game_display.blit(self.black_pieces[piece_type], (self.cell_size * y, self.cell_size * (7 - x)))


def main():
    PlayGame(True)


if __name__ == "__main__":
    main()
