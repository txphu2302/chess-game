Chess Game
A simple chess game implemented using Python and Pygame, featuring a graphical interface and AI opponents with adjustable difficulty levels.
Description
This project is a 2D chess game where players can play against an AI or watch two AIs compete in a demo mode. The game includes:

Human vs AI Mode: Play as White or Black against an AI with three difficulty levels (Easy, Medium, Hard).
AI vs AI Demo Mode: Watch AI White (using selected difficulty) compete against AI Black (using Easy/Random logic).
Features: Move validation, check/checkmate detection, promotion selection, sound effects, and a simple AI based on minimax with alpha-beta pruning.

Installation
Prerequisites

Python 3.x
Required libraries:
pygame
python-chess



Setup

Clone the repository:
git clone https://github.com/username/ChessGame.git
cd ChessGame


Install dependencies:
pip install pygame python-chess


Ensure the assets folder contains:

Sound files: move-self.wav, capture.wav, castle.wav, move-check.wav
Piece images: wP.png, wN.png, wB.png, wR.png, wQ.png, wK.png, bP.png, bN.png, bB.png, bR.png, bQ.png, bK.png
(If missing, the game will use fallback text-based images.)


Run the game:
python chess_game.py



Usage
Main Menu

Human vs AI: Select your color (White, Black, or Random) and difficulty (Easy, Medium, Hard, or Random).
AI vs AI (Demo): Watch two AIs play, with White using the selected difficulty and Black using Easy/Random logic.
Exit Game: Quit the application.

In-Game

Click on a piece to select it, then click a valid destination square to move.
Promotion: When a pawn reaches the opponent's end, choose a piece (Queen, Rook, Bishop, Knight) from the promotion menu.
Game Over: Displayed when checkmate, stalemate, or draw occurs, with options to play again or return to the main menu.
Info Panel: Shows whose turn it is, difficulty, and buttons for New Game or Main Menu.

Controls

Mouse: Click to select and move pieces.
Buttons: Use on-screen buttons for menu navigation and game actions.

Features

Difficulty Levels:
Easy: Random moves with 70% chance to capture.
Medium: Basic minimax with depth 1.
Hard: Minimax with alpha-beta pruning and depth 3.


AI vs AI Demo: White AI uses the selected difficulty, Black AI uses Easy/Random logic.
Visuals: Highlighted selected squares, last move, and check status.
Sound Effects: Move, capture, castle, and check sounds (if assets are available).

Development
Contributing
Feel free to fork this repository and submit pull requests. Suggestions for improvements (e.g., better AI, GUI enhancements) are welcome!
Change Log

05/03/2025: Adjusted AI vs AI Demo mode - White uses Hard, Black uses Easy Random logic. Improved promotion menu alignment and game over screen to show the last move.

Known Issues

Sound effects require specific asset files; missing files trigger fallback mode.
AI performance may slow down at higher difficulties due to minimax depth.

License
[MIT License] 

Contact
For questions or support, contact [toilaphu23@example.com] or open an issue on this repository.
