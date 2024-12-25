import numpy as np
import pygame
import sys
import random 
from threading import Timer
import math

# Constants
# row and column count
ROWS = 6
COLS = 7

# turns
PLAYER_TURN = 0
AI_TURN = 1

# pieces represented as numbers
PLAYER_PIECE = 1
AI_PIECE = 2

# colors for GUI
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# size of one game location
SQUARESIZE = 100

# dimensions for pygame GUI
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
CIRCLE_RADIUS = int(SQUARESIZE/2 - 5)
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)

# Constants
WINDOW_LEN = 4


def create_board():
    return np.zeros((ROWS, COLS))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[0][col] == 0


def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            return row


def winning_move(board, piece):
    """
    Checks if the current board state results in a winning move for the given piece.
    """
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    # Vertical Check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Positive Slope Diagonal Check
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    # Negative Slope Diagonal Check
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    return False


def draw_board(board):
    """
    Draws the game board using Pygame.
    """
    for col in range(COLS):
        for row in range(ROWS):
            pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, row * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            color = BLACK  # Default empty slot
            if board[row][col] == PLAYER_PIECE:
                color = RED
            elif board[row][col] == AI_PIECE:
                color = YELLOW
            pygame.draw.circle(screen, color, (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), CIRCLE_RADIUS)
    pygame.display.update()
    

def get_valid_locations(board):
    valid_locations = []
    
    for column in range(COLS):
        if is_valid_location(board, column):
            valid_locations.append(column)

    return valid_locations

# Utility Functions
def is_terminal_node(board):
    return (
        winning_move(board, PLAYER_PIECE) or
        winning_move(board, AI_PIECE) or
        len(get_valid_locations(board)) == 0
    )

def score_window(window, piece):
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    score = 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 20
    return score

def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Score Horizontal
    for row in range(ROWS):
        row_array = [board[row][col] for col in range(COLS)]
        for col in range(COLS - WINDOW_LEN + 1):
            window = row_array[col:col + WINDOW_LEN]
            score += score_window(window, piece)

    # Score Vertical
    for col in range(COLS):
        col_array = [board[row][col] for row in range(ROWS)]
        for row in range(ROWS - WINDOW_LEN + 1):
            window = col_array[row:row + WINDOW_LEN]
            score += score_window(window, piece)

    # Score Positive Diagonals
    for row in range(ROWS - WINDOW_LEN + 1):
        for col in range(COLS - WINDOW_LEN + 1):
            window = [board[row + i][col + i] for i in range(WINDOW_LEN)]
            score += score_window(window, piece)

    # Score Negative Diagonals
    for row in range(WINDOW_LEN - 1, ROWS):
        for col in range(COLS - WINDOW_LEN + 1):
            window = [board[row - i][col + i] for i in range(WINDOW_LEN)]
            score += score_window(window, piece)

    return score



def end_game():
    global game_over
    game_over = True
    print(game_over)
    