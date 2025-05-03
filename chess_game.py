import pygame
import chess
import sys
import time
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 640, 640
INFO_HEIGHT = 60
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_HEIGHT))
pygame.display.set_caption("Chess Game")

# Colors
LIGHT_SQUARE = pygame.Color(240, 217, 181)
DARK_SQUARE = pygame.Color(181, 136, 99)
HIGHLIGHT_COLOR = pygame.Color(186, 202, 68)
LAST_MOVE_COLOR = pygame.Color(205, 210, 106, 150)
CHECK_COLOR = pygame.Color(240, 84, 84, 180)
INFO_BG_COLOR = pygame.Color(50, 50, 50)
TEXT_COLOR = pygame.Color(255, 255, 255)
BUTTON_COLOR = pygame.Color(70, 130, 180)
BUTTON_HOVER_COLOR = pygame.Color(100, 149, 237)
MENU_BG_COLOR = pygame.Color(40, 40, 40)
TITLE_COLOR = pygame.Color(255, 215, 0)

# Sounds
try:
    MOVE_SOUND = pygame.mixer.Sound("assets/move-self.wav")
    CAPTURE_SOUND = pygame.mixer.Sound("assets/capture.wav")
    CASTLE_SOUND = pygame.mixer.Sound("assets/castle.wav")
    CHECK_SOUND = pygame.mixer.Sound("assets/move-check.wav")
except:
    print("Warning: Sound files not found. Game will run without sound effects.")
    MOVE_SOUND = None
    CAPTURE_SOUND = None
    CASTLE_SOUND = None
    CHECK_SOUND = None

# Load piece images
images = {}
def load_images():
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K']
    for piece in pieces:
        for color in ['w', 'b']:
            name = color + piece
            try:
                images[name] = pygame.transform.scale(
                    pygame.image.load(f"assets/{name}.png"), (SQUARE_SIZE, SQUARE_SIZE)
                )
            except FileNotFoundError:
                img = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                font = pygame.font.SysFont("arial", 36)
                text = font.render(name, True, pygame.Color("black") if color == 'w' else pygame.Color("white"))
                img.fill(pygame.Color("white") if color == 'w' else pygame.Color("black"))
                img.blit(text, (SQUARE_SIZE//2 - text.get_width()//2, SQUARE_SIZE//2 - text.get_height()//2))
                images[name] = img
                print(f"Warning: Image assets/{name}.png not found. Using fallback image.")

# Button class for menus
class Button:
    def __init__(self, rect, text, font_size=24, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("arial", font_size)
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

# Main menu screen
def show_main_menu():
    button_width, button_height = 300, 60
    x_pos = WIDTH // 2 - button_width // 2
    
    human_vs_ai_button = Button(
        pygame.Rect(x_pos, 250, button_width, button_height),
        "Human vs AI"
    )
    
    ai_vs_ai_button = Button(
        pygame.Rect(x_pos, 330, button_width, button_height),
        "AI vs AI (Demo)"
    )
    
    exit_button = Button(
        pygame.Rect(x_pos, 410, button_width, button_height),
        "Exit Game"
    )
    
    buttons = [human_vs_ai_button, ai_vs_ai_button, exit_button]
    
    running = True
    selected_mode = None
    
    while running:
        screen.fill(MENU_BG_COLOR)
        
        font_title = pygame.font.SysFont("arial", 48, bold=True)
        title_text = font_title.render("Chess Game", True, TITLE_COLOR)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        
        font_version = pygame.font.SysFont("arial", 18)
        version_text = font_version.render("v1.1", True, TEXT_COLOR)
        screen.blit(version_text, (WIDTH - version_text.get_width() - 10, HEIGHT + INFO_HEIGHT - version_text.get_height() - 10))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if human_vs_ai_button.handle_event(event):
                selected_mode = "human_vs_ai"
                running = False
            elif ai_vs_ai_button.handle_event(event):
                selected_mode = "ai_vs_ai"
                running = False
            elif exit_button.handle_event(event):
                return None
        
        pygame.time.Clock().tick(60)
    
    return selected_mode

# Color selection screen
def show_color_selection():
    button_width, button_height = 300, 60
    x_pos = WIDTH // 2 - button_width // 2
    
    white_button = Button(
        pygame.Rect(x_pos, 250, button_width, button_height),
        "Play as White"
    )
    
    black_button = Button(
        pygame.Rect(x_pos, 330, button_width, button_height),
        "Play as Black"
    )
    
    random_button = Button(
        pygame.Rect(x_pos, 410, button_width, button_height),
        "Random Color"
    )
    
    back_button = Button(
        pygame.Rect(x_pos, 490, button_width, button_height),
        "Back to Main Menu",
        color=pygame.Color(150, 50, 50)
    )
    
    buttons = [white_button, black_button, random_button, back_button]
    
    running = True
    selected_color = None
    
    while running:
        screen.fill(MENU_BG_COLOR)
        
        font_title = pygame.font.SysFont("arial", 48, bold=True)
        title_text = font_title.render("Select Your Color", True, TITLE_COLOR)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if white_button.handle_event(event):
                selected_color = "white"
                running = False
            elif black_button.handle_event(event):
                selected_color = "black"
                running = False
            elif random_button.handle_event(event):
                selected_color = "white" if random.random() > 0.5 else "black"
                running = False
            elif back_button.handle_event(event):
                return "back"
        
        pygame.time.Clock().tick(60)
    
    return selected_color

# Difficulty selection screen
def show_difficulty_menu(mode):
    button_width, button_height = 300, 60
    x_pos = WIDTH // 2 - button_width // 2
    
    easy_button = Button(
        pygame.Rect(x_pos, 250, button_width, button_height),
        "Easy"
    )
    
    medium_button = Button(
        pygame.Rect(x_pos, 330, button_width, button_height),
        "Medium"
    )
    
    hard_button = Button(
        pygame.Rect(x_pos, 410, button_width, button_height),
        "Hard"
    )
    
    random_button = Button(
        pygame.Rect(x_pos, 490, button_width, button_height),
        "Random Mode"
    )
    
    back_button = Button(
        pygame.Rect(x_pos, 570, button_width, button_height),
        "Back",
        color=pygame.Color(150, 50, 50)
    )
    
    buttons = [easy_button, medium_button, hard_button, random_button, back_button]
    
    running = True
    selected_difficulty = None
    
    while running:
        screen.fill(MENU_BG_COLOR)
        
        font_title = pygame.font.SysFont("arial", 48, bold=True)
        title_text = font_title.render("Select Difficulty", True, TITLE_COLOR)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        
        font_mode = pygame.font.SysFont("arial", 24)
        mode_text = "Human vs AI" if mode == "human_vs_ai" else "AI vs AI Demo"
        mode_render = font_mode.render(f"Mode: {mode_text}", True, TEXT_COLOR)
        screen.blit(mode_render, (WIDTH // 2 - mode_render.get_width() // 2, 170))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if easy_button.handle_event(event):
                selected_difficulty = "easy"
                running = False
            elif medium_button.handle_event(event):
                selected_difficulty = "medium"
                running = False
            elif hard_button.handle_event(event):
                selected_difficulty = "hard"
                running = False
            elif random_button.handle_event(event):
                difficulties = ["easy", "medium", "hard"]
                selected_difficulty = random.choice(difficulties)
                font_notification = pygame.font.SysFont("arial", 36)
                notification = font_notification.render(f"Selected: {selected_difficulty.capitalize()}", True, TITLE_COLOR)
                screen.blit(notification, (WIDTH // 2 - notification.get_width() // 2, HEIGHT - 100))
                pygame.display.flip()
                time.sleep(1.5)
                running = False
            elif back_button.handle_event(event):
                return "back"
        
        pygame.time.Clock().tick(60)
    
    return selected_difficulty

# Draw chessboard
def draw_board():
    for r in range(8):
        for c in range(8):
            color = LIGHT_SQUARE if (r + c) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    font = pygame.font.SysFont("arial", 12)
    for i in range(8):
        file_text = font.render(chr(97 + i), True, DARK_SQUARE if i % 2 == 0 else LIGHT_SQUARE)
        screen.blit(file_text, (i * SQUARE_SIZE + SQUARE_SIZE - 12, HEIGHT - 12))
        
        rank_text = font.render(str(8 - i), True, DARK_SQUARE if i % 2 == 1 else LIGHT_SQUARE)
        screen.blit(rank_text, (5, i * SQUARE_SIZE + 5))

# Draw pieces
def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            color = 'w' if piece.color == chess.WHITE else 'b'
            img = images[color + piece.symbol().upper()]
            screen.blit(img, (col*SQUARE_SIZE, row*SQUARE_SIZE))

# Highlight selected square and valid moves
def draw_highlights(board, selected_square, last_move):
    if selected_square is not None:
        col = chess.square_file(selected_square)
        row = 7 - chess.square_rank(selected_square)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
        
        for move in board.legal_moves:
            if move.from_square == selected_square:
                to_square = move.to_square
                to_col = chess.square_file(to_square)
                to_row = 7 - chess.square_rank(to_square)
                
                if board.piece_at(to_square):
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, 
                                   (to_col*SQUARE_SIZE, to_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
                else:
                    pygame.draw.circle(screen, HIGHLIGHT_COLOR,
                                     (to_col*SQUARE_SIZE + SQUARE_SIZE//2, to_row*SQUARE_SIZE + SQUARE_SIZE//2), 
                                     SQUARE_SIZE//6)
    
    if last_move:
        for square in [last_move.from_square, last_move.to_square]:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(LAST_MOVE_COLOR)
            screen.blit(s, (col*SQUARE_SIZE, row*SQUARE_SIZE))
    
    if board.is_check():
        king_square = board.king(board.turn)
        col = chess.square_file(king_square)
        row = 7 - chess.square_rank(king_square)
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(CHECK_COLOR)
        screen.blit(s, (col*SQUARE_SIZE, row*SQUARE_SIZE))

# Draw info panel
def draw_info_panel(board, difficulty, mode, player_color=None):
    pygame.draw.rect(screen, INFO_BG_COLOR, (0, HEIGHT, WIDTH, INFO_HEIGHT))
    
    font = pygame.font.SysFont("arial", 20)
    
    if mode == "human_vs_ai":
        if player_color == "white":
            turn_text = "White (Human) to move" if board.turn == chess.WHITE else "Black (AI) thinking..."
        else:
            turn_text = "White (AI) thinking..." if board.turn == chess.WHITE else "Black (Human) to move"
    else:
        turn_text = "White (AI) thinking..." if board.turn == chess.WHITE else "Black (Random AI) thinking..."
    
    if board.is_check():
        turn_text += " - CHECK!"
    if board.is_checkmate():
        winner = "White" if board.turn == chess.BLACK else "Black"
        turn_text = f"Checkmate! {winner} wins!"
    elif board.is_stalemate():
        turn_text = "Stalemate! Draw!"
    elif board.is_insufficient_material():
        turn_text = "Draw due to insufficient material!"
    elif board.can_claim_draw():
        turn_text = "Draw claim available (50-move rule or repetition)"
    
    status_text = font.render(turn_text, True, TEXT_COLOR)
    screen.blit(status_text, (20, HEIGHT + 20))
    
    diff_text = font.render(f"Difficulty: {difficulty.capitalize()}", True, TEXT_COLOR)
    screen.blit(diff_text, (WIDTH - diff_text.get_width() - 20, HEIGHT + 20))
    
    button_width = 120
    restart_button = pygame.Rect(WIDTH // 2 - button_width - 10, HEIGHT + 15, button_width, 30)
    menu_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT + 15, button_width, 30)
    
    if restart_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, restart_button)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
    
    if menu_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, menu_button)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, menu_button)
    
    restart_text = font.render("New Game", True, TEXT_COLOR)
    menu_text = font.render("Main Menu", True, TEXT_COLOR)
    
    screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, 
                            restart_button.centery - restart_text.get_height() // 2))
    screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, 
                          menu_button.centery - menu_text.get_height() // 2))
    
    return restart_button, menu_button

# Promotion selection screen
def show_promotion_menu(piece_color):
    overlay = pygame.Surface((WIDTH, HEIGHT + INFO_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    promo_box = pygame.Rect(WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2)
    pygame.draw.rect(screen, MENU_BG_COLOR, promo_box)
    pygame.draw.rect(screen, TITLE_COLOR, promo_box, 4)
    
    font_title = pygame.font.SysFont("arial", 36, bold=True)
    title_text = font_title.render("Select Promotion", True, TITLE_COLOR)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4 + 20))
    
    button_width, button_height = 80, 80
    spacing = 20
    x_start = WIDTH//2 - (button_width * 2 + spacing) // 2
    y_start = HEIGHT//4 + 80
    
    queen_button = Button(
        pygame.Rect(x_start, y_start, button_width, button_height),
        "Queen",
        font_size=16
    )
    rook_button = Button(
        pygame.Rect(x_start + button_width + spacing, y_start, button_width, button_height),
        "Rook",
        font_size=16
    )
    bishop_button = Button(
        pygame.Rect(x_start, y_start + button_height + spacing, button_width, button_height),
        "Bishop",
        font_size=16
    )
    knight_button = Button(
        pygame.Rect(x_start + button_width + spacing, y_start + button_height + spacing, button_width, button_height),
        "Knight",
        font_size=16
    )
    
    buttons = [queen_button, rook_button, bishop_button, knight_button]
    
    running = True
    selected_piece = None
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)
            
            if button == queen_button:
                img = images[f"{piece_color}Q"]
            elif button == rook_button:
                img = images[f"{piece_color}R"]
            elif button == bishop_button:
                img = images[f"{piece_color}B"]
            elif button == knight_button:
                img = images[f"{piece_color}N"]
            
            img_scaled = pygame.transform.scale(img, (button_width - 20, button_height - 20))
            img_rect = img_scaled.get_rect(center=(button.rect.centerx, button.rect.centery - 10))
            screen.blit(img_scaled, img_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if queen_button.handle_event(event):
                selected_piece = chess.QUEEN
                running = False
            elif rook_button.handle_event(event):
                selected_piece = chess.ROOK
                running = False
            elif bishop_button.handle_event(event):
                selected_piece = chess.BISHOP
                running = False
            elif knight_button.handle_event(event):
                selected_piece = chess.KNIGHT
                running = False
        
        pygame.time.Clock().tick(60)
    
    return selected_piece

# Game result screen
def show_game_result(board, last_move, result, mode, difficulty):
    draw_board()
    draw_highlights(board, None, last_move)
    draw_pieces(board)
    draw_info_panel(board, difficulty, mode)
    
    overlay = pygame.Surface((WIDTH, HEIGHT + INFO_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    result_box = pygame.Rect(WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2)
    pygame.draw.rect(screen, MENU_BG_COLOR, result_box)
    pygame.draw.rect(screen, TITLE_COLOR, result_box, 4)
    
    font_title = pygame.font.SysFont("arial", 36, bold=True)
    font_info = pygame.font.SysFont("arial", 24)
    
    title_text = font_title.render("Game Over", True, TITLE_COLOR)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4 + 30))
    
    result_text = font_info.render(result, True, TEXT_COLOR)
    screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//4 + 100))
    
    mode_text = "Human vs AI" if mode == "human_vs_ai" else "AI vs AI Demo"
    mode_render = font_info.render(f"Mode: {mode_text}", True, TEXT_COLOR)
    screen.blit(mode_render, (WIDTH//2 - mode_render.get_width()//2, HEIGHT//4 + 150))
    
    diff_render = font_info.render(f"Difficulty: {difficulty.capitalize()}", True, TEXT_COLOR)
    screen.blit(diff_render, (WIDTH//2 - diff_render.get_width()//2, HEIGHT//4 + 190))
    
    button_width, button_height = 200, 50
    play_again_button = Button(
        pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//4 + 250, button_width, button_height),
        "Play Again"
    )
    
    main_menu_button = Button(
        pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//4 + 320, button_width, button_height),
        "Main Menu"
    )
    
    buttons = [play_again_button, main_menu_button]
    
    running = True
    action = None
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if play_again_button.handle_event(event):
                action = "play_again"
                running = False
            elif main_menu_button.handle_event(event):
                action = "main_menu"
                running = False
        
        pygame.time.Clock().tick(60)
    
    return action

# Piece-square tables
piece_square_tables = {
    chess.PAWN: [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ],
    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ],
    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5,  5,  5,  5,  5,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ],
    chess.ROOK: [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ],
    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],
    chess.KING: [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20
    ]
}

# End game king piece square table
king_endgame_table = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

# Piece values
piece_values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, 
                chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}

# Global transposition table
transposition_table = {}

# Evaluate move for sorting
def evaluate_move(board, move):
    score = 0
    try:
        if board.is_capture(move):
            victim_piece = board.piece_at(move.to_square)
            attacker_piece = board.piece_at(move.from_square)
            if victim_piece and attacker_piece:
                score += 10 * piece_values.get(victim_piece.piece_type, 0) - piece_values.get(attacker_piece.piece_type, 0) / 10
        
        if move.promotion:
            score += 900
        
        board.push(move)
        if board.is_check():
            score += 50
        board.pop()
        
        piece = board.piece_at(move.from_square)
        if piece and (piece.piece_type == chess.PAWN or piece.piece_type == chess.KNIGHT):
            to_file = chess.square_file(move.to_square)
            to_rank = chess.square_rank(move.to_square)
            center_distance = abs(3.5 - to_file) + abs(3.5 - to_rank)
            score += (4 - center_distance) * 5
    
    except Exception as e:
        print(f"Error in evaluate_move: {str(e)}")
    
    return score

# Improved board evaluation
def evaluate_board(board, difficulty):
    try:
        if board.is_checkmate():
            return -10000 if board.turn == chess.WHITE else 10000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0
        
        for piece_type in piece_values:
            white_pieces = len(board.pieces(piece_type, chess.WHITE))
            black_pieces = len(board.pieces(piece_type, chess.BLACK))
            score += piece_values[piece_type] * (white_pieces - black_pieces)
        
        if difficulty != "easy":
            for piece_type in piece_square_tables:
                if piece_type == chess.KING and len(list(board.piece_map().keys())) <= 12:
                    for square in board.pieces(piece_type, chess.WHITE):
                        if 0 <= square <= 63:
                            score += king_endgame_table[square] / 10
                    for square in board.pieces(piece_type, chess.BLACK):
                        if 0 <= square <= 63:
                            score -= king_endgame_table[63 - square] / 10
                else:
                    for square in board.pieces(piece_type, chess.WHITE):
                        if 0 <= square <= 63:
                            score += piece_square_tables[piece_type][square] / 10
                    for square in board.pieces(piece_type, chess.BLACK):
                        if 0 <= square <= 63:
                            score -= piece_square_tables[piece_type][63 - square] / 10
        
        if difficulty == "hard":
            current_turn = board.turn
            board.turn = chess.WHITE
            white_mobility = len(list(board.legal_moves))
            board.turn = chess.BLACK
            black_mobility = len(list(board.legal_moves))
            board.turn = current_turn
            score += (white_mobility - black_mobility) * 0.1
            
            white_king_square = board.king(chess.WHITE)
            black_king_square = board.king(chess.BLACK)
            
            if white_king_square in [chess.G1, chess.C1]:
                score += 30
            if black_king_square in [chess.G8, chess.C8]:
                score -= 30
            
            center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
            for square in center_squares:
                piece = board.piece_at(square)
                if piece:
                    score += 10 if piece.color == chess.WHITE else -10
                
                for pawn_square in board.pieces(chess.PAWN, chess.WHITE):
                    pawn_file = chess.square_file(pawn_square)
                    pawn_rank = chess.square_rank(pawn_square)
                    if 2 <= pawn_file <= 5 and 3 <= pawn_rank <= 4:
                        score += 5
                
                for pawn_square in board.pieces(chess.PAWN, chess.BLACK):
                    pawn_file = chess.square_file(pawn_square)
                    pawn_rank = chess.square_rank(pawn_square)
                    if 2 <= pawn_file <= 5 and 3 <= pawn_rank <= 4:
                        score -= 5
            
            if len(list(board.piece_map().keys())) > 28:
                developed_white = 0
                developed_black = 0
                for square, piece in [(chess.B1, chess.KNIGHT), (chess.G1, chess.KNIGHT), 
                                    (chess.C1, chess.BISHOP), (chess.F1, chess.BISHOP)]:
                    if not board.piece_at(square) or board.piece_at(square).piece_type != piece:
                        developed_white += 1
                for square, piece in [(chess.B8, chess.KNIGHT), (chess.G8, chess.KNIGHT), 
                                    (chess.C8, chess.BISHOP), (chess.F8, chess.BISHOP)]:
                    if not board.piece_at(square) or board.piece_at(square).piece_type != piece:
                        developed_black += 1
                score += developed_white * 10
                score -= developed_black * 10
        
        return score
    
    except Exception as e:
        print(f"Error in evaluate_board: {str(e)}")
        return 0

# Alpha-Beta with memory
def alpha_beta_with_memory(board, depth, alpha, beta, is_max, difficulty):
    board_hash = board.fen()
    
    try:
        if board_hash in transposition_table and transposition_table[board_hash]["depth"] >= depth:
            return transposition_table[board_hash]["score"]
        
        if depth == 0 or board.is_game_over():
            score = evaluate_board(board, difficulty)
            transposition_table[board_hash] = {"score": score, "depth": depth}
            return score
        
        if is_max:
            max_eval = float('-inf')
            moves = list(board.legal_moves)
            if not moves:
                print("Error: No legal moves in alpha_beta_with_memory (max)")
                return evaluate_board(board, difficulty)
            
            move_scores = [(move, evaluate_move(board, move)) for move in moves]
            sorted_moves = [move for move, score in sorted(move_scores, key=lambda x: -x[1])]
            
            for move in sorted_moves:
                board.push(move)
                eval = alpha_beta_with_memory(board, depth - 1, alpha, beta, False, difficulty)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            
            transposition_table[board_hash] = {"score": max_eval, "depth": depth}
            return max_eval
        else:
            min_eval = float('inf')
            moves = list(board.legal_moves)
            if not moves:
                print("Error: No legal moves in alpha_beta_with_memory (min)")
                return evaluate_board(board, difficulty)
            
            move_scores = [(move, evaluate_move(board, move)) for move in moves]
            sorted_moves = [move for move, score in sorted(move_scores, key=lambda x: -x[1])]
            
            for move in sorted_moves:
                board.push(move)
                eval = alpha_beta_with_memory(board, depth - 1, alpha, beta, True, difficulty)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            
            transposition_table[board_hash] = {"score": min_eval, "depth": depth}
            return min_eval
    
    except Exception as e:
        print(f"Error in alpha_beta_with_memory (depth: {depth}, is_max: {is_max}): {str(e)}")
        return evaluate_board(board, difficulty)

# AI move with error handling
def make_ai_move(board, difficulty):
    if board.is_game_over():
        return None
    
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        print("Error: No legal moves available!")
        return None
    
    try:
        if difficulty == "easy":
            captures = [move for move in legal_moves if board.is_capture(move)]
            if captures and random.random() < 0.7:
                move = random.choice(captures)
            else:
                move = random.choice(legal_moves)
            return move
        
        elif difficulty == "hard":
            best_move = None
            best_score = float('-inf') if board.turn == chess.WHITE else float('inf')
            alpha = float('-inf')
            beta = float('inf')
            
            if len(transposition_table) > 100000:
                transposition_table.clear()
            
            moves = legal_moves
            move_scores = [(move, evaluate_move(board, move)) for move in moves]
            sorted_moves = [move for move, score in sorted(move_scores, key=lambda x: -x[1])]
            
            for depth in range(1, 4):
                if board.turn == chess.WHITE:
                    best_score = float('-inf')
                    for move in sorted_moves:
                        board.push(move)
                        score = alpha_beta_with_memory(board, depth, alpha, beta, False, difficulty)
                        board.pop()
                        if score > best_score:
                            best_score = score
                            best_move = move
                        alpha = max(alpha, score)
                else:
                    best_score = float('inf')
                    for move in sorted_moves:
                        board.push(move)
                        score = alpha_beta_with_memory(board, depth, alpha, beta, True, difficulty)
                        board.pop()
                        if score < best_score:
                            best_score = score
                            best_move = move
                        beta = min(beta, score)
            return best_move
        
        else:  # medium
            best_move = None
            best_score = float('-inf') if board.turn == chess.WHITE else float('inf')
            
            moves = legal_moves
            move_scores = [(move, evaluate_move(board, move)) for move in moves]
            sorted_moves = [move for move, score in sorted(move_scores, key=lambda x: -x[1])]
            
            for move in sorted_moves:
                board.push(move)
                if board.turn == chess.WHITE:
                    score = alpha_beta_with_memory(board, 1, float('-inf'), float('inf'), False, difficulty)
                    if score > best_score:
                        best_score = score
                        best_move = move
                else:
                    score = alpha_beta_with_memory(board, 1, float('-inf'), float('inf'), True, difficulty)
                    if score < best_score:
                        best_score = score
                        best_move = move
                board.pop()
            return best_move
    
    except Exception as e:
        print(f"Error in make_ai_move (difficulty: {difficulty}): {str(e)}")
        return None

# Main game function (Adjusted for AI vs AI Demo)
def play_game(mode, difficulty, player_color=None):
    board = chess.Board()
    selected_square = None
    last_move = None
    promotion_pending = False
    pending_move = None
    
    if mode == "human_vs_ai" and player_color == "black" and board.turn == chess.WHITE:
        ai_move = make_ai_move(board, difficulty)
        if ai_move:
            board.push(ai_move)
            last_move = ai_move
            if MOVE_SOUND:
                MOVE_SOUND.play()
    
    clock = pygame.time.Clock()
    running = True
    ai_thinking = False
    ai_move_time = 0
    
    while running:
        draw_board()
        draw_highlights(board, selected_square, last_move)
        draw_pieces(board)
        restart_button, menu_button = draw_info_panel(board, difficulty, mode, player_color)
        
        if promotion_pending:
            piece_color = 'w' if board.turn == chess.WHITE else 'b'
            promotion_choice = show_promotion_menu(piece_color)
            if promotion_choice is None:
                return "quit"
            
            final_move = chess.Move(pending_move.from_square, pending_move.to_square, promotion=promotion_choice)
            board.push(final_move)
            last_move = final_move
            if MOVE_SOUND:
                MOVE_SOUND.play()
            
            promotion_pending = False
            pending_move = None
            if board.is_check() and CHECK_SOUND:
                CHECK_SOUND.play()
            pygame.display.flip()
            continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if mode == "human_vs_ai" and ((player_color == "white" and board.turn == chess.WHITE) or 
                                        (player_color == "black" and board.turn == chess.BLACK)):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        file = x // SQUARE_SIZE
                        rank = 7 - (y // SQUARE_SIZE)
                        square = chess.square(file, rank)
                        
                        piece = board.piece_at(square)
                        if selected_square is None:
                            if piece and piece.color == board.turn:
                                selected_square = square
                        else:
                            move = chess.Move(selected_square, square)
                            piece = board.piece_at(selected_square)
                            
                            is_promotion = False
                            if piece and piece.piece_type == chess.PAWN:
                                if (piece.color == chess.WHITE and chess.square_rank(square) == 7) or \
                                   (piece.color == chess.BLACK and chess.square_rank(square) == 0):
                                    is_promotion = True
                            
                            if is_promotion:
                                promotion_pending = True
                                pending_move = move
                                continue
                            else:
                                if move in board.legal_moves:
                                    if board.is_capture(move):
                                        if CAPTURE_SOUND:
                                            CAPTURE_SOUND.play()
                                    elif board.is_castling(move):
                                        if CASTLE_SOUND:
                                            CASTLE_SOUND.play()
                                    else:
                                        if MOVE_SOUND:
                                            MOVE_SOUND.play()
                                    
                                    board.push(move)
                                    last_move = move
                                    selected_square = None
                                    
                                    if board.is_check():
                                        if CHECK_SOUND:
                                            CHECK_SOUND.play()
                                else:
                                    if piece and piece.color == board.turn:
                                        selected_square = square
                                    else:
                                        selected_square = None
                    else:
                        selected_square = None
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    return "restart"
                elif menu_button.collidepoint(mouse_pos):
                    return "menu"
        
        if not board.is_game_over():
            if mode == "ai_vs_ai":
                # In AI vs AI mode, White uses the selected difficulty, Black uses "easy" (Random)
                current_difficulty = difficulty if board.turn == chess.WHITE else "easy"
            else:
                # In Human vs AI mode, use the selected difficulty for the AI
                current_difficulty = difficulty if ((player_color == "white" and board.turn == chess.BLACK) or 
                                                    (player_color == "black" and board.turn == chess.WHITE)) else None
            
            if current_difficulty:
                if not ai_thinking:
                    ai_thinking = True
                    ai_move_time = time.time() + 0.5
                
                elif time.time() > ai_move_time:
                    ai_move = make_ai_move(board, current_difficulty)
                    if ai_move:
                        if board.is_capture(ai_move):
                            if CAPTURE_SOUND:
                                CAPTURE_SOUND.play()
                        elif board.is_castling(ai_move):
                            if CASTLE_SOUND:
                                CASTLE_SOUND.play()
                        else:
                            if MOVE_SOUND:
                                MOVE_SOUND.play()
                        
                        board.push(ai_move)
                        last_move = ai_move
                        if board.is_check():
                            if CHECK_SOUND:
                                CHECK_SOUND.play()
                    else:
                        print("Warning: AI failed to produce a move")
                    ai_thinking = False
        
        if board.is_game_over():
            pygame.display.flip()
            time.sleep(1)
            
            if board.is_checkmate():
                winner = "White" if board.turn == chess.BLACK else "Black"
                result_message = f"Checkmate! {winner} wins!"
            elif board.is_stalemate():
                result_message = "Stalemate! It's a draw!"
            elif board.is_insufficient_material():
                result_message = "Draw due to insufficient material!"
            elif board.can_claim_draw():
                result_message = "Draw (50-move rule or repetition)"
            else:
                result_message = "Game over!"
            
            result = show_game_result(board, last_move, result_message, mode, difficulty)
            return result
        
        pygame.display.flip()
        clock.tick(60)
    
    return "quit"

# Main function
def main():
    load_images()
    action = None
    
    while True:
        mode = show_main_menu() if action != "quit" else None
        if mode is None:
            break
        
        player_color = None
        if mode == "human_vs_ai":
            player_color = show_color_selection()
            if player_color == "back" or player_color is None:
                continue
        
        difficulty = show_difficulty_menu(mode)
        if difficulty == "back" or difficulty is None:
            continue
        
        action = play_game(mode, difficulty, player_color)
        
        if action == "quit":
            break
        elif action == "menu" or action == "main_menu":
            continue
        elif action == "restart":
            action = play_game(mode, difficulty, player_color)

# Entry point
if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        sys.exit()