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
            col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)

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
            
main()