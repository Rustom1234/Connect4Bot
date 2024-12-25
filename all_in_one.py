import numpy as np
import pygame
import sys
import random 

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
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)
SIZE = (width, height)
screen = pygame.display.set_mode(SIZE)

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
            pygame.draw.circle(screen, color, (col * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), circle_radius)
    pygame.display.update()
    



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
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            _, new_score = minimax(b_copy, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:  # Prune branches
                break
        return best_col, value
    else:
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            _, new_score = minimax(b_copy, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:  # Prune branches
                break
        return best_col, value

def get_valid_locations(board):
    valid_locations = []
    
    for column in range(COLS):
        if is_valid_location(board, column):
            valid_locations.append(column)

    return valid_locations

from board import create_board, draw_board, drop_piece, is_valid_location, get_next_open_row, winning_move
from minimax import minimax
import numpy as np
import pygame
import sys
import random
from threading import Timer
import math  
    
def end_game():
    global game_over
    game_over = True
    print(game_over)
    
"""def main():
    global game_over
    game_over = False  # Initialize the game_over variable
    
    ROWS = 6
    COLS = 7
    SQUARESIZE = 100
    PLAYER_PIECE = 1
    AI_PIECE = 2
    WIDTH = COLS * SQUARESIZE
    HEIGHT = (ROWS + 1) * SQUARESIZE
    SIZE = (WIDTH, HEIGHT)
    # turns
    PLAYER_TURN = 0
    AI_TURN = 1
    # Colors
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    ver = True
    not_over = True  # Add initialization for not_over

    board = create_board()

    # initial turn is random
    turn = random.randint(PLAYER_TURN, AI_TURN)

    # initializing pygame
    pygame.init()

    # size of one game location
    SQUARESIZE = 100

    # dimensions for pygame GUI
    width = COLS * SQUARESIZE
    height = (ROWS + 1) * SQUARESIZE
    circle_radius = int(SQUARESIZE / 2 - 5)
    size = (width, height)
    screen = pygame.display.set_mode(size)

    # font for win message
    my_font = pygame.font.SysFont("monospace", 75)

    # draw GUI
    draw_board(board)
    pygame.display.update()

    # game loop
    # -------------------------------
    while not game_over:

        # for every player event
        for event in pygame.event.get():

            # if player closes the window
            if event.type == pygame.QUIT:
                sys.exit()

            # if player moves the mouse, their piece moves at the top of the screen
            if event.type == pygame.MOUSEMOTION and not_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                xpos = pygame.mouse.get_pos()[0]
                if turn == PLAYER_TURN:
                    pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE / 2)), circle_radius)

            # if player clicks the button, we drop their piece down
            if event.type == pygame.MOUSEBUTTONDOWN and not_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # ask for player 1 input
                if turn == PLAYER_TURN:
                    xpos = event.pos[0]
                    col = int(math.floor(xpos / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
                        if winning_move(board, PLAYER_PIECE):
                            print("PLAYER 1 WINS!")
                            label = my_font.render("PLAYER 1 WINS!", 1, RED)
                            screen.blit(label, (40, 10))
                            not_over = False
                            t = Timer(3.0, end_game)
                            t.start()

                    draw_board(board)

                    # increment turn by 1
                    turn += 1

                    # this will alternate between 0 and 1 with every turn
                    turn = turn % 2

            pygame.display.update()

        # if it's the AI's turn
        if turn == AI_TURN and not game_over and not_over:

            # the column to drop in is found using minimax
            col, minimax_score = minimax(board, 7, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    print("PLAYER 2 WINS!")
                    label = my_font.render("PLAYER 2 WINS!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, end_game)
                    t.start()
            draw_board(board)

            # increment turn by 1
            turn += 1
            # this will alternate between 0 and 1 with every turn
            turn = turn % 2
            """



def main():
    # Initialize game variables
    global game_over
    game_over = False  # Keeps track of whether the game has ended

    # Initialize game board
    board = create_board()
    draw_board(board)

    # Turn management
    PLAYER_TURN = 0
    AI_TURN = 1
    turn = random.randint(PLAYER_TURN, AI_TURN)  # Randomize first turn

    # Initialize Pygame
    pygame.init()

    # Define GUI properties
    SQUARESIZE = 100
    WIDTH = COLS * SQUARESIZE
    HEIGHT = (ROWS + 1) * SQUARESIZE
    RADIUS = SQUARESIZE // 2 - 5
    SIZE = (WIDTH, HEIGHT)

    # Set up Pygame window
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Connect 4")
    my_font = pygame.font.SysFont("monospace", 75)

    # Draw the initial board
    draw_board(board)
    pygame.display.update()

    # Game loop
    while not game_over:
        for event in pygame.event.get():
            # Handle quitting
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Player interaction: moving the piece on mouse movement
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                xpos = event.pos[0]
                if turn == PLAYER_TURN:
                    pygame.draw.circle(screen, RED, (xpos, SQUARESIZE // 2), RADIUS)
                pygame.display.update()

            # Player interaction: placing a piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == PLAYER_TURN:
                    xpos = event.pos[0]
                    col = int(xpos // SQUARESIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        # Check for a win
                        if winning_move(board, PLAYER_PIECE):
                            print("PLAYER 1 WINS!")
                            label = my_font.render("PLAYER 1 WINS!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        draw_board(board)

                        # Switch turns
                        turn = AI_TURN

        # AI interaction
        if turn == AI_TURN and not game_over:
            pygame.time.wait(500)
            col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                # Check for a win
                if winning_move(board, AI_PIECE):
                    print("PLAYER 2 WINS!")
                    label = my_font.render("PLAYER 2 WINS!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(board)

                # Switch turns
                turn = PLAYER_TURN

        # End game delay
        if game_over:
            pygame.time.wait(3000)
            
main()