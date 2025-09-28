import pygame 
import sys
import math

WIDTH ,HEIGHT = 300, 400
LINE_WIDTH = 7
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CROSS_WIDTH = 25

BG_COLOR = (159, 37, 150)
LINE_COLOR = (135, 31, 135)
CIRCLE_COLOR = (255, 255, 255)
CROSS_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

pygame.init()
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
font = pygame.font.SysFont('Arial', 30, True)

board=[" " for _ in range(9)]
game_over = False
winner = None

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 3 * SQUARE_SIZE), (WIDTH, 3 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, WIDTH), LINE_WIDTH)

def draw_figure():
    for i in range(9):
        row , col= i//3 , i%3

        if board[i]=='X':
            start_dsc= (col * SQUARE_SIZE + 25, row * SQUARE_SIZE + 25)
            end_dsc = (col * SQUARE_SIZE + SQUARE_SIZE - 25, row * SQUARE_SIZE + SQUARE_SIZE - 25)
            start_asc= (col * SQUARE_SIZE + 25, row * SQUARE_SIZE + SQUARE_SIZE - 25)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - 25, row * SQUARE_SIZE + 25)
            pygame.draw.line(screen, CROSS_COLOR, start_dsc, end_dsc, CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        elif board[i]=='O':
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CROSS_WIDTH)

def check_win(player, board_state):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board_state[condition[0]] == board_state[condition[1]] == board_state[condition[2]] == player:
            return True
    return False
def is_board_full(board_state):
    return " " not in board_state

def minimax(board_copy, is_maximizing):
    """The core recursive function of the AI."""
    if check_win('O', board_copy): return 1      # AI ('O') wins, this is a great outcome (+1)
    if check_win('X', board_copy): return -1     # Player ('X') wins, this is a terrible outcome (-1)
    if is_board_full(board_copy): return 0       # It's a tie, this is a neutral outcome (0)

    if is_maximizing:
        best_score = -math.inf  
        for i in range(9):
            if board_copy[i] == ' ':
                board_copy[i] = 'O'  
                score = minimax(board_copy, False) 
                board_copy[i] = ' '  
                best_score = max(score, best_score) 
        return best_score
    
    else:
        best_score = math.inf 
        for i in range(9):
            if board_copy[i] == ' ':
                board_copy[i] = 'X'
                score = minimax(board_copy, True) 
                board_copy[i] = ' ' 
                best_score = min(score, best_score) 
        return best_score

def ai_move():
    """The function that decides and makes the AI's move."""
    best_score = -math.inf 
    best_move = -1
    
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(list(board), False)
            board[i] = ' '

            if score > best_score:
                best_score = score
                best_move = i
                
    if best_move != -1:
        board[best_move] = 'O'

def display_message(message):
    """Displays a message at the bottom of the screen."""
    pygame.draw.rect(screen, BG_COLOR, (0, 300, 300, 100))
    
    text = font.render(message, True, TEXT_COLOR)
    
    text_rect = text.get_rect(center=(WIDTH / 2, 350))
    
    screen.blit(text, text_rect)

def restart_game():
    """Resets the game state for a new game."""
    global board, game_over, winner
    
    board = [' ' for _ in range(9)]
    game_over = False
    winner = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            index = clicked_row * BOARD_COLS + clicked_col
            if board[index] == " ":
                board[index] = 'X'
                if check_win('X', board):
                    winner = 'You'
                    game_over = True
                elif is_board_full(board):
                    winner = 'Tie'
                    game_over = True
                else:
                    ai_move() 

                    if check_win('O', board):
                        winner = 'AI'
                        game_over = True
                    elif is_board_full(board):
                        winner = 'Tie'
                        game_over = True

        if event.type == pygame.KEYDOWN:
            # If the key is 'R', call the restart function
            if event.key == pygame.K_r:
                restart_game()
        screen.fill(BG_COLOR)
        draw_lines()
        draw_figure()

        if game_over:
            if winner == 'Tie':
                display_message("It's a Tie! (R to restart)")
            else:
                display_message(f"{winner} wins! (R to restart)")
        pygame.display.update()
