from board import create_board, draw_board, drop_piece, is_valid_location, get_next_open_row, winning_move
from minimax import ai_move
import numpy as np
import pygame
import sys

def select_game_mode():
    """
    Allows the user to select the game mode.
    Returns:
        mode (str): The selected game mode - 'pvp', 'pvai', 'aivai'.
    """
    print("Select Game Mode:")
    print("1. Player vs Player (PvP)")
    print("2. Player vs AI (PvAI)")
    print("3. AI vs AI (AIvAI)")
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == "1":
        return "pvp"
    elif choice == "2":
        return "pvai"
    elif choice == "3":
        return "aivai"
    else:
        print("Invalid choice. Defaulting to PvP.")
        return "pvp"
    
def main():
    ROWS = 6
    COLS = 7
    SQUARESIZE = 100
    PLAYER_PIECE = 1
    AI_PIECE = 2
    WIDTH = COLS * SQUARESIZE
    HEIGHT = (ROWS + 1) * SQUARESIZE
    SIZE = (WIDTH, HEIGHT)

    pygame.init()
    
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Connect Four")
    
    board = create_board()
    draw_board(board, screen)
    pygame.display.update()
    
    game_over = False
    turn = 0

    # Select game mode
    mode = select_game_mode()

    while not game_over:
        # Player vs Player Mode
        if mode == "pvp":
            if turn == 0:
                col = int(input("Player 1 Make your Selection (1-7): ")) - 1
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        print("PLAYER 1 WINS!")
                        game_over = True
            else:
                col = int(input("Player 2 Make your Selection (1-7): ")) - 1
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)
                    if winning_move(board, AI_PIECE):
                        print("PLAYER 2 WINS!")
                        game_over = True

        # Player vs AI Mode
        elif mode == "pvai":
            if turn == 0:
                col = int(input("Player Make your Selection (1-7): ")) - 1
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        print("PLAYER WINS!")
                        game_over = True
            else:
                col = ai_move(board, AI_PIECE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)
                    if winning_move(board, AI_PIECE):
                        print("AI WINS!")
                        game_over = True

        # AI vs AI Mode
        elif mode == "aivai":
            col = ai_move(board, AI_PIECE)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    print("AI WINS!")
                    game_over = True

        turn += 1
        turn = turn % 2
        draw_board(board, screen)

if __name__ == "__main__":
    main()