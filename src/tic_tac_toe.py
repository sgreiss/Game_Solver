import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Board
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = 1  # 1 = X, -1 = O
game_over = False

def draw_lines():
    # Horizontal
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

    # Vertical
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                # Draw X
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
            elif board[row][col] == -1:
                # Draw O
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_winner():
    # Horizontal
    for row in board:
        if sum(row) == 3:
            return 1
        if sum(row) == -3:
            return -1
        
    # Vertical
    for col in range(BOARD_COLS):
        col_sum = board[0][col] + board[1][col] + board[2][col]
        if col_sum == 3:
            return 1
        if col_sum == -3:
            return -1
        
    # Diagonals
    diag1 = board[0][0] + board[1][1] + board[2][2]
    diag2 = board[0][2] + board[1][1] + board[2][0]
    if diag1 == 3 or diag2 == 3:
        return 1
    if diag1 == -3 or diag2 == -3:
        return -1
    return 0

def is_full():
    return all(cell != 0 for row in board for cell in row)

def reset_game():
    global board, player, game_over
    board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = 1
    game_over = False
    screen.fill(BG_COLOR)
    draw_lines()

def ai_make_move():
    empty_cells = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = -1
        draw_figures()
        return True
    return False


# Main loop
draw_lines()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            row = mouseY // SQUARE_SIZE
            col = mouseX // SQUARE_SIZE

            if board[row][col] == 0:
                board[row][col] = 1  # Player X
                draw_figures()

                winner = check_winner()
                if winner == 1:
                    print("Player X wins!")
                    game_over = True
                elif is_full():
                    print("It's a draw!")
                    game_over = True
                else:
                    ai_make_move()

                    winner = check_winner()
                    if winner == -1:
                        print("Player O (AI) wins!")
                        game_over = True
                    elif is_full():
                        print("It's a draw!")
                        game_over = True


        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            reset_game()

    pygame.display.update()
