import numpy as np
import pygame
import sys

# Constants
ROWS = 6
COLS = 7

SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 5
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode(SIZE)


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
            pygame.draw.circle(screen, color, (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
    pygame.display.update()
    
