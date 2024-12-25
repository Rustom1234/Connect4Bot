import math
import random
from board import *

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

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    # Base Case: Terminal Node or Depth Reached
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = np.copy(board)
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(value, alpha)
            if alpha >= beta:  # Prune branches
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = np.copy(board)
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(value, beta)
            if alpha >= beta:  # Prune branches
                break
        return best_col, value