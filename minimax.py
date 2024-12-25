import math
import random
from board import *

# Constants
WINDOW_LEN = 4
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
ROWS = 6
COLS = 7

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
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 8
    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [board[row][COLS // 2] for row in range(ROWS)]
    score += center_array.count(piece) * 6

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

def minimax(board, depth, maximizing_player, alpha, beta):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    # Base Case: Terminal Node or Depth Reached
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 1000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -1000000
            else:
                return None, 0
        else:
            return None, score_position(board, AI_PIECE)

    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            _, new_score = minimax(temp_board, depth - 1, False, alpha, beta)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            _, new_score = minimax(temp_board, depth - 1, True, alpha, beta)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]