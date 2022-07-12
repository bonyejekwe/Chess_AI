# Chess AI
**Must run _pip install pygame_**

The program is known to work with python version 3.7. We do not guarantee any other version of python will work with our program.

To play the game with the GUI:
1) Run: Project/displayGame.py
2) The console will prompt you to select a side to play on. Input 1 to play as white, or -1 to play as black, and then hit ENTER
3) The console will then prompt you to select an AI to play against. Select 1 to play against the Minimax AI, and 2 to play against the Monte Carlo Tree Search AI. Then, hit ENTER
4) A new window will appear. If it does not pop up, then you may have to click on the icon on the taskbar at the bottom or top of the screen
5) If you chose to play as white, you move first. If you chose to play as black, the AI will move first. It is possible that the AI has already made its first move before the window pops up.
6) When moving a piece: select the piece you would like to move. The piece's tile will light up green, indicating that it has been selected. Select another tile where you would like to move to. If the piece does not move to the selected tile, it is not a legal move, and you will have to select a new move to make. 
7) If you already selected a piece but instead would like to move a different piece, or if the piece you originally selected has no legal moves, then you can deselect the original piece selected by clicking again on the selected tile.
8) The amount of time it takes for the computer to make a move depends on the AI you play against, but it should not take more than 30 seconds.
9) To exit out of the game, either use the x arrow in the top corner, or just force quit the program.
10) Once the game is over, the display of the board will automatically close, not showing the resutling board. You are able to see the final values in the output of the python console. **The output displayed in the python console is upside down compared to what is displayed on the gui**. The output in the console will also show the winner of the game. The numbers are as follows: 1 is white won, -1 is black won, 2 is white put black in stalemate, -2 is black put white in stalemate, 0 is a draw. A draw is triggered either by no piece being captured in 50 consecutive moves, or 25 for each player, or there were 200 moves in total.

This is a continuation of a final group project for DS3500: Advanced Programming with Data at Northeastern University. That project was created by [Adrian Monaghan](https://github.com/adrianmonaghan), [Nicholas Gjuraj](https://github.com/nicholasgjuraj), [Maxwell Arnold](https://github.com/maxwellarnold24), and [myself](https://github.com/bonyejekwe), and the link to the commit for the final submission is found [here](https://github.com/bonyejekwe/Chess_AI/tree/4a2f4e1d44659b38e7ec3af9c2d2b1e31449cb29).
https://github.com/adrianmonaghan
