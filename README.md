# Connect 4 Bot using MiniMax Algorithm #

<img src="Screenshot 2024-12-26 at 9.10.49 PM.png" alt="Connect 4 Bot" width="450"/>

## Introduction

Connect 4 Bot using Minimax Algorithm is a classic implementation of Connect 4 in Python, featuring a Graphical User Interface (GUI) using the pygame library and allows a user to play against an AI opponent powered by the MiniMax Algorithm with alpha-beta pruning. Due to the simple nature of Connect 4 and the fact that if both players play a perfect game, the starting player will always win, the bot can definitely by beaten if the player starts first. This game is designed for players to test themselves against a computer opponent and gain a better understanding of the game. 

## Installation

1. Clone the Repository and Change Directory
```
git clone https://github.com/yourusername/Connect4Bot.git
cd Connect4Bot
```
2. Install Dependencies
```
pip install -r requirements.txt
```

## Usage

1. Run the game
```
python main.py
```
2. Gameplay Instructions
-Player 1 (Red): Click on the desired column to drop your red piece.
- AI (Yellow): The AI will automatically make its move after yours.
- Winning the Game: Align four of your pieces horizontally, vertically, or diagonally.
- Draw: If the board is full and no player has four aligned pieces, the game ends in a draw.
3. Exiting the Game
- Click the close button on the game window or press Ctrl + C in the terminal to exit.

## Gameplay

<img src="Screenshot 2024-12-26 at 9.38.27 PM.png" alt="Connect 4 Bot Start" width="450"/>

1. Starting the Game
- Upon launching, the game window displays an empty Connect 4 board. A random player (either the human or AI) starts the game.
2. Making a Move
- Player's Turn: Move your mouse to select the desired column and click to drop your piece.
- AI's Turn: The AI calculates and drops its piece automatically.
3. Winning the Game
- Once a player aligns four pieces, a winning message is displayed, and the game ends after a short delay.
4. Draw Scenario
- If all columns are filled without any player winning, a draw message is shown.

## Code Structure

This code is organised with into three main classes to ensure readability and modularity:

1. The `Board` class 
Contains all the functions that create the board, allow players to drop pieces, calculate Win, Loss, or Draw situations and scoring various possible positions on the board. 
2. The `Minimax` class
Contains the minimax function with alpha-beta pruning. 
3. The `Game` class
Contains the `end_game` and `run` functions where the `run` function acts as a standard main function that uses the `Board` and `Minimax` classes to run the game using pygame.

## Project Structure

```
Connect4Bot/
├── images_of_app/
│   └── matches.csv
├── data/
│   ├── ipl_data_2016.csv
│   └── matches.csv
├── code/
│   ├── app.py
│   └── model_pipeline.py
├── model_pipeline/
│   └── ipl_pipeline.pkl
├──.gitattributes
├── requirements.txt
└── README.md
```