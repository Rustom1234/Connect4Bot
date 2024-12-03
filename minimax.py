import random
from board import *


window_len = 4
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
ROWS = 6
COLS = 7

def is_end(board):
    return (
        winning_move(board, PLAYER_PIECE) or
        winning_move(board, AI_PIECE) or
        len(get_valid_locations(board)) == 0
    )
    
def detect_trap(board, opponent_piece):
    """
    Detects if the opponent has a trap (two consecutive winning moves).
    Returns True if a trap is detected; otherwise, False.
    """
    for col in range(COLS):
        temp_board = board.copy()
        if is_valid_location(temp_board, col):
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, opponent_piece)
            if winning_move(temp_board, opponent_piece):  # Opponent wins immediately
                return True
    return False

def score_window(window, piece):
    
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    
    if window.count(piece) == 4:
        score += 200
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score    

def score_moves(board, piece):
    
    score = 0

    #Logic here: The center is always stronger to play pieces as 4 connections can be made from anywhere on the board, so center is prioritised
    center_arr = [row[4] for row in board]
    center_count = center_arr.count(piece)
    score += center_count * 3
    
    #Evaluate all possible situations
    #Horizontals
    for row in range(ROWS):
        row_array = [board[row][col] for col in range(COLS)]
        for col in range(COLS):
            window = row_array[col: col + window_len]
            score += score_window(window, piece)
    
    #Verticals
    for col in range(COLS):
        col_array = [board[row][col] for row in range(ROWS)]
        for row in range(ROWS):
            window = col_array[row: row + window_len]
            score += score_window(window, piece)
            
    #Diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(window_len)]
            score += score_window(window, piece)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col - i] for i in range(window_len)]
            score += score_window(window, piece)
            
    return score
    
def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]
    
    
    
    
"""
Creating the minimax algorithm with alpha beta pruning
"""

MAX = float('inf')
MIN = float('inf')

def minimax(board, depth, maxPlayer, alpha, beta):
    valid_locations = get_valid_locations(board)
    end_game = is_end(board)
    
    if depth == 0 or end_game:
        if end_game:
            if winning_move(board, AI_PIECE):
                return None, float('inf')
            elif winning_move(board, PLAYER_PIECE):
                return None, - float('inf')
            else:
                return None, 0
        return None, score_moves(board, AI_PIECE)
    
    if maxPlayer:
        best = MIN
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            _, new_score = minimax(temp_board, depth - 1, False, alpha, beta)
            if new_score > best:
                best = new_score
                best_col = col
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best_col, best
    
    else:
        best = MAX
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            _, new_score = minimax(temp_board, depth - 1, True, alpha, beta)
            if new_score < best:
                best = new_score
                best_col = col
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best_col, best
        
            
def ai_move(board, piece, depth=5):
    #Get Ideal AI move
    col, _ = minimax(board, depth, True, -float('inf'), float('inf'))
    return col
