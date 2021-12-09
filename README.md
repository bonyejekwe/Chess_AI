# Chess AI
**Use main branch**

**Must run _pip install pygame_**

The program is known to work with python version 3.7. We do not guarantee any other version of python will work with our program.
To play the game with the gui:
1) Run: Project/displayGame.py
2) An output will appear in the console asking you to input 1 to play as white, or -1 to play as black. Make the decision and input the value, then hit enter
3) A new window will appear, it may not come forward and therefore you may have to click on the icon on the taskbar at the bottom or top of the screen
4) If you chose white, you move first, select the piece you would like to move, it's background will light up green, select the tile you would like to move it to
5) If you chose black, the computer moves first, it will make a move, there is a chance that by the time you opened the window the AI has already made its first move
6) When you move a piece: select the piece you would like to move, its tile will light up green indicating the tile/piece you have selected. Select another tile where you would like to move to. If the piece does not move to the selected tile, it is not a legal move, and therefore, you must select a new legal space. 
7) If you already selected a piece but instead would like to move a different piece, or the piece you originally selected has no legal moves, you can deselect the original piece selected by clicking again on the selected tile.
8) When the computer moves it takes at least a few seconds. It can take upwards of 10 to 20 possibly more seconds. Be patient. If it is taking too long always feel free to just exit out of the game either using the x arrow or just force closing it. Windows may say the process is not responsing, ignore it.
9) Once the game is over, the display of the board will automatically close, not showing the resutling board. You are able to see the final values in the output of the python console. **The output displayed in the python console is upside down compared to what is displayed on the gui**. The output in the console will also show the winner of the game. The numbers are as follows: 1 is white won, -1 is black won, 2 is white put black in stalemate, -2 is black put white in stalemate, 0 is a draw. A draw is triggered either by no piece being captured in 50 consecutive moves, or 25 for each player, or there were 200 moves in total.

To play the game against itself:
1) Run: Project/game.py
2) The way the file is currently set up, white will be our best AI playing against a randomly moving opponent playing as black piece. 
3) If you would like to change the file to have different set ups that is possible, however, you must read the comments on the file to have any chance of getting it to work properly **This file is mainly for our testing purposes only, and therefore, does not have the proper error catching or detection that is normally required of a user facing file. Therefore, editing this file will be at your own risk**

**Project/main.py is only meant for testing the game and is therefore not meant to be run. It will not break anything if you do, however, it is of no use to a regular user**

Please reach out to us with any questions or issues that we may be able to resolve. Our emails are:
monaghan.ad@northeastern.edu onyejekwe.b@northeastern.edu gjuraj.n@northeastern.edu arnold.m@northeastern.edu
