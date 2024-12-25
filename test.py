N = """ I lifted this code:
# for representing the board as a matrix and doing operations on it
import numpy as np
# for gui
import pygame
# for exiting the gui
import sys
# for calulations, for exampel with infinity
import math
# for delaying execution of certain events
from threading import Timer
# for generating random values, for example for 1st turn
import random
# global constant variables
# -------------------------------
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
# various functions used by the game
# -------------------------------

# using numpy, create an empty matrix of 6 rows and 7 columns
def create_board():
    board = np.zeros((ROWS, COLS))
    return board


# add a piece to a given location, i.e., set a position in the matrix as 1 or 2
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# checking that the top row of the selected column is still not filled
# i.e., that there is still space in the current column
# note that indexing starts at 0
def is_valid_location(board, col):
    return board[0][col] == 0


# checking where the piece will fall in the current column
# i.e., finding the first zero row in the given column
def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r


# calculating if the current state of the board for player or AI is a win
def winning_move(board, piece):
    # checking horizontal 'windows' of 4 for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking vertical 'windows' of 4 for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # checking positively sloped diagonals for win
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    # checking negatively sloped diagonals for win
    for c in range(3,COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True


# visually representing the board using pygame
# for each position in the matrix the board is either filled with an empty black circle, or a palyer/AI red/yellow circle
def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else :
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()


# evaluate a 'window' of 4 locations in a row based on what pieces it contains
# the values used can be experimented with
def evaluate_window(window, piece):
    # by default the oponent is the player
    opponent_piece = PLAYER_PIECE

    # if we are checking from the player's perspective, then the oponent is AI
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    # initial score of a window is 0
    score = 0

    # based on how many friendly pieces there are in the window, we increase the score
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # or decrese it if the oponent has 3 in a row
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4 

    return score    


# scoring the overall attractiveness of a board after a piece has been droppped
def score_position(board, piece):

    score = 0

    # score center column --> we are prioritizing the central column because it provides more potential winning windows
    center_array = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # below we go over every single window in different directions and adding up their values to the score
    # score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # score positively sloped diagonals
    for r in range(3,ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # score negatively sloped diagonals
    for r in range(3,ROWS):
        for c in range(3,COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# checking if the given turn or in other words node in the minimax tree is terminal
# a terminal node is player winning, AI winning or board being filled up
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# The algorithm calculating the best move to make given a depth of the search tree.
# Depth is how many layers algorithm scores boards. Complexity grows exponentially.
# Alpha and beta are best scores a side can achieve assuming the opponent makes the best play.
# More on alpha-beta pruning here: https://www.youtube.com/watch?v=l-hh51ncgDI.
# maximizing_palyer is a boolean value that tells whether we are maximizing or minimizing
# in this implementation, AI is maximizing.
def minimax(board, depth, alpha, beta, maximizing_player):

    # all valid locations on the board
    valid_locations = get_valid_locations(board)

    # boolean that tells if the current board is terminal
    is_terminal = is_terminal_node(board)

    # if the board is terminal or depth == 0
    # we score the win very high and a draw as 0
    if depth == 0 or is_terminal:
        if is_terminal: # winning move 
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        # if depth is zero, we simply score the current board
        else: # depth is zero
            return (None, score_position(board, AI_PIECE))

    # if the current board is not rerminal and we are maximizing
    if maximizing_player:

        # initial value is what we do not want - negative infinity
        value = -math.inf

        # this will be the optimal column. Initially it is random
        column = random.choice(valid_locations)

        # for every valid column, we simulate dropping a piece with the help of a board copy
        # and run the minimax on it with decresed depth and switched player
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            # recursive call
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            # if the score for this column is better than what we already have
            if new_score > value:
                value = new_score
                column = col
            # alpha is the best option we have overall
            alpha = max(value, alpha) 
            # if alpha (our current move) is greater (better) than beta (opponent's best move), then 
            # the oponent will never take it and we can prune this branch
            if alpha >= beta:
                break

        return column, value
    
    # same as above, but for the minimizing player
    else: # for thte minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta) 
            if alpha >= beta:
                break
        return column, value


# get all columns where a piece can be
def get_valid_locations(board):
    valid_locations = []
    
    for column in range(COLS):
        if is_valid_location(board, column):
            valid_locations.append(column)

    return valid_locations


# end the game which will close the window eventually
def end_game():
    global game_over
    game_over = True
    print(game_over)


# various state tracker variables taht use the above fucntions
# -------------------------------

# initializing the board
board = create_board()

# initially nobody has won yet
game_over = False

# initially the game is not over - this is used for GUI quirks
not_over = True

# initial turn is random
turn = random.randint(PLAYER_TURN, AI_TURN)

# initializing pygame
pygame.init()

# size of one game location
SQUARESIZE = 100

# dimensions for pygame GUI
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)

# font for win message
my_font = pygame.font.SysFont("monospace", 75)

# draw GUI
draw_board(board)
pygame.display.update()


# game loop
# -------------------------------

# loop that runs while the game_over variable is false,
# i.e., someone hasn't placed 4 in a row yet
while not game_over:

    # for every player event
    for event in pygame.event.get():

        # if player clses the window
        if event.type == pygame.QUIT:
            sys.exit()

        # if player moves the mouse, their piece moves at the top of the screen
        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            xpos = pygame.mouse.get_pos()[0]
            if turn == PLAYER_TURN:
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius )

        # if player clicks the button, we drop their piece down
        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

            # ask for player 1 inupt
            if turn == PLAYER_TURN:

                # we assume players will use correct input
                xpos = event.pos[0] 
                col = int(math.floor(xpos/SQUARESIZE)) 

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

                # this will alternate between 0 and 1 withe very turn
                turn = turn % 2 

        pygame.display.update()

                     
    # if its the AI's turn
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
        # this will alternate between 0 and 1 withe very turn
        turn = turn % 2


Now my code is these 3 files:

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
    
    # Check horizontal locations
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    # Check vertical locations
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Check positive diagonals
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    # Check negative diagonals
    for col in range(3, COLS):
        for row in range(3, ROWS):
            if all(board[row - i][col - i] == piece for i in range(4)):
                return True

    return False


def draw_board(board):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, (row + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[row][col] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
            elif board[row][col] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
            else:
                pygame.draw.circle(screen, BLACK, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
    pygame.display.update()
    

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
    
    
"""
"""


def score_window(window, piece):
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    piece_count = window.count(piece)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opp_piece)
    
    if piece_count == 4:
        return 200
    elif piece_count == 3 and empty_count == 1:
        return 20
    elif piece_count == 2 and empty_count == 2:
        return 6
    elif opp_count == 3 and empty_count == 1:
        return -12  # Block opponent's winning move
    return 0


def score_moves(board, piece):
    
    score = 0
    center_col = [board[row][COLS // 2] for row in range(ROWS)]
    center_count = center_col.count(piece)
    score += center_count * 6  # Increased center priority
    
    #Evaluate all possible situations
    #Horizontals
    for row in range(ROWS):
        for col in range(COLS - window_len + 1):    #Should be cols from 0 to 4 (not including 4)
            window = [board[row][col + i] for i in range(window_len)]
            score += score_window(window, piece)
    
    #Verticals
    for col in range(COLS):
        for row in range(ROWS - window_len + 1):
            window = [board[row + i][col] for i in range(window_len)]
            score += score_window(window, piece)
            
    #Create all Diagonals First to make scoring faster
    #Positive diagonals
    diagonals = []
    diagonals = []
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            diagonals.append([board[row - i][col + i] for i in range(window_len)])  # Positive slope
        for row in range(3, ROWS):
            diagonals.append([board[row - i][col - i] for i in range(window_len)])  # Negative slope
    for each_window in diagonals:
        score += score_window(each_window, piece)
        
    return score
    
    
def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]
    
    
    
    

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
                return None, -float('inf')
            else:
                return None, 0
        return None, score_moves(board, AI_PIECE)
    
    if maxPlayer:
        best = -float('inf')
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
    
def main():
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
            
main()

The code I lifted works and the ai works well. My ai does not work, it loses every time"""

s = ""
for line in N.split('\n'):
    if line != '\n':
        s += "\n" + line 

print(s)
        