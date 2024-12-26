import pygame
import math
import numpy as np
import random
import sys
from threading import Timer

ROWS = 6
COLS = 7

PLAYER_TURN = 0
AI_TURN = 1

PLAYER_PIECE = 1
AI_PIECE = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SQUARESIZE = 100
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
CIRCLE_RADIUS = int(SQUARESIZE / 2 - 5)
SIZE = (WIDTH, HEIGHT)

WINDOW_LEN = 4


class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        return np.zeros((ROWS, COLS))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                return row
        return None  

    def winning_move(self, piece):
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(self.board[row][col + i] == piece for i in range(4)):
                    return True

        for col in range(COLS):
            for row in range(ROWS - 3):
                if all(self.board[row + i][col] == piece for i in range(4)):
                    return True

        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    return True

        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(self.board[row + i][col + i] == piece for i in range(4)):
                    return True

        return False

    def get_valid_locations(self):
        return [col for col in range(COLS) if self.is_valid_location(col)]

    def is_terminal_node(self):
        return (
            self.winning_move(PLAYER_PIECE) or
            self.winning_move(AI_PIECE) or
            len(self.get_valid_locations()) == 0
        )

    def score_window(self, window, piece):
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

    def score_position(self, piece):
        score = 0
        
        center_array = [int(i) for i in list(self.board[:, COLS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 6

        for row in range(ROWS):
            row_array = [int(i) for i in list(self.board[row, :])]
            for col in range(COLS - WINDOW_LEN + 1):
                window = row_array[col:col + WINDOW_LEN]
                score += self.score_window(window, piece)

        for col in range(COLS):
            col_array = [int(i) for i in list(self.board[:, col])]
            for row in range(ROWS - WINDOW_LEN + 1):
                window = col_array[row:row + WINDOW_LEN]
                score += self.score_window(window, piece)

        for row in range(ROWS - WINDOW_LEN + 1):
            for col in range(COLS - WINDOW_LEN + 1):
                window = [self.board[row + i][col + i] for i in range(WINDOW_LEN)]
                score += self.score_window(window, piece)

        for row in range(WINDOW_LEN - 1, ROWS):
            for col in range(COLS - WINDOW_LEN + 1):
                window = [self.board[row - i][col + i] for i in range(WINDOW_LEN)]
                score += self.score_window(window, piece)

        return score

    def draw_board(self, screen, font):
        for col in range(COLS):
            for row in range(ROWS):
                pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, row * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                color = BLACK  
                if self.board[row][col] == PLAYER_PIECE:
                    color = RED
                elif self.board[row][col] == AI_PIECE:
                    color = YELLOW
                pygame.draw.circle(screen, color, (
                    int(col * SQUARESIZE + SQUARESIZE / 2),
                    int(row * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                   CIRCLE_RADIUS)
        pygame.display.update()


class AI:
    def __init__(self, depth=6):
        self.depth = depth

    def minimax(self, board: Board, depth, alpha, beta, maximizing_player):
        valid_locations = board.get_valid_locations()
        is_terminal = board.is_terminal_node()

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.winning_move(AI_PIECE):
                    return (None, 1000000)
                elif board.winning_move(PLAYER_PIECE):
                    return (None, -1000000)
                else:  
                    return (None, 0)
            else:  
                return (None, board.score_position(AI_PIECE))

        if maximizing_player:
            value = -math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                if row is not None:
                    temp_board = Board()
                    temp_board.board = np.copy(board.board)
                    temp_board.drop_piece(row, col, AI_PIECE)
                    new_score = self.minimax(temp_board, depth - 1, alpha, beta, False)[1]
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
                row = board.get_next_open_row(col)
                if row is not None:
                    temp_board = Board()
                    temp_board.board = np.copy(board.board)
                    temp_board.drop_piece(row, col, PLAYER_PIECE)
                    new_score = self.minimax(temp_board, depth - 1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        best_col = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break  
            return best_col, value


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Connect 4")
        self.my_font = pygame.font.SysFont("monospace", 75)
        self.board = Board()
        self.ai = AI(depth=6)
        self.game_over = False
        self.not_over = True
        self.turn = random.randint(PLAYER_TURN, AI_TURN)
        self.clock = pygame.time.Clock()

    def end_game(self):
        self.game_over = True
        print("Game Over!")

    def run(self):
        self.board.draw_board(self.screen, self.my_font)
        pygame.display.update()

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION and self.not_over:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                    xpos = event.pos[0]
                    if self.turn == PLAYER_TURN:
                        pygame.draw.circle(self.screen, RED, (xpos, int(SQUARESIZE / 2)), CIRCLE_RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and self.not_over:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                    if self.turn == PLAYER_TURN:
                        xpos = event.pos[0]
                        col = int(math.floor(xpos / SQUARESIZE))

                        if self.board.is_valid_location(col):
                            row = self.board.get_next_open_row(col)
                            if row is not None:
                                self.board.drop_piece(row, col, PLAYER_PIECE)

                                if self.board.winning_move(PLAYER_PIECE):
                                    print("PLAYER 1 WINS!")
                                    label = self.my_font.render("PLAYER 1 WINS!", 1, RED)
                                    self.screen.blit(label, (40, 10))
                                    self.board.draw_board(self.screen, self.my_font)
                                    self.not_over = False
                                    Timer(3.0, self.end_game).start()

                                self.board.draw_board(self.screen, self.my_font)
                                self.turn = (self.turn + 1) % 2

            if self.turn == AI_TURN and not self.game_over and self.not_over:
                col, minimax_score = self.ai.minimax(self.board, self.ai.depth, -math.inf, math.inf, True)

                if self.board.is_valid_location(col):
                    pygame.time.wait(500)
                    row = self.board.get_next_open_row(col)
                    if row is not None:
                        self.board.drop_piece(row, col, AI_PIECE)

                        if self.board.winning_move(AI_PIECE):
                            print("PLAYER 2 WINS!")
                            label = self.my_font.render("PLAYER 2 WINS!", 1, YELLOW)
                            self.screen.blit(label, (40, 10))
                            self.board.draw_board(self.screen, self.my_font)
                            self.not_over = False
                            Timer(3.0, self.end_game).start()

                        self.board.draw_board(self.screen, self.my_font)
                        self.turn = (self.turn + 1) % 2

            if not self.board.get_valid_locations() and self.not_over:
                print("It's a Draw!")
                label = self.my_font.render("DRAW!", 1, YELLOW)
                self.screen.blit(label, (40, 10))
                self.board.draw_board(self.screen, self.my_font)
                self.not_over = False
                Timer(3.0, self.end_game).start()
            self.clock.tick(60) 


if __name__ == "__main__":
    game = Game()
    game.run()