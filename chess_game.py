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
pygame.display.set_caption("Chess: Human vs AI")

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
                # Create a fallback image with text
                img = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                font = pygame.font.SysFont("arial", 36)
                text = font.render(name, True, pygame.Color("black") if color == 'w' else pygame.Color("white"))
                img.fill(pygame.Color("white") if color == 'w' else pygame.Color("black"))
                img.blit(text, (SQUARE_SIZE//2 - text.get_width()//2, SQUARE_SIZE//2 - text.get_height()//2))
                images[name] = img
                print(f"Warning: Image assets/{name}.png not found. Using fallback image.")

# Draw chessboard
def draw_board():
    for r in range(8):
        for c in range(8):
            color = LIGHT_SQUARE if (r + c) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    # Draw board coordinates
    font = pygame.font.SysFont("arial", 12)
    for i in range(8):
        # Files (a-h)
        file_text = font.render(chr(97 + i), True, DARK_SQUARE if i % 2 == 0 else LIGHT_SQUARE)
        screen.blit(file_text, (i * SQUARE_SIZE + SQUARE_SIZE - 12, HEIGHT - 12))
        
        # Ranks (1-8)
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
    # Highlight selected square
    if selected_square is not None:
        col = chess.square_file(selected_square)
        row = 7 - chess.square_rank(selected_square)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
        
        # Highlight possible moves
        for move in board.legal_moves:
            if move.from_square == selected_square:
                to_square = move.to_square
                to_col = chess.square_file(to_square)
                to_row = 7 - chess.square_rank(to_square)
                
                # Different highlight for captures
                if board.piece_at(to_square):
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, 
                                   (to_col*SQUARE_SIZE, to_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
                else:
                    pygame.draw.circle(screen, HIGHLIGHT_COLOR,
                                     (to_col*SQUARE_SIZE + SQUARE_SIZE//2, to_row*SQUARE_SIZE + SQUARE_SIZE//2), 
                                     SQUARE_SIZE//6)
    
    # Highlight last move
    if last_move:
        for square in [last_move.from_square, last_move.to_square]:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(LAST_MOVE_COLOR)
            screen.blit(s, (col*SQUARE_SIZE, row*SQUARE_SIZE))
    
    # Highlight king in check
    if board.is_check():
        king_square = board.king(board.turn)
        col = chess.square_file(king_square)
        row = 7 - chess.square_rank(king_square)
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(CHECK_COLOR)
        screen.blit(s, (col*SQUARE_SIZE, row*SQUARE_SIZE))

# Draw info panel
def draw_info_panel(board, difficulty):
    # Draw background
    pygame.draw.rect(screen, INFO_BG_COLOR, (0, HEIGHT, WIDTH, INFO_HEIGHT))
    
    # Draw status
    font = pygame.font.SysFont("arial", 20)
    turn_text = "White to move" if board.turn == chess.WHITE else "Black (AI) thinking..."
    if board.is_check():
        turn_text += " - CHECK!"
    if board.is_checkmate():
        turn_text = "Checkmate! " + ("White wins!" if board.turn == chess.BLACK else "Black wins!")
    elif board.is_stalemate():
        turn_text = "Stalemate! Draw!"
    elif board.is_insufficient_material():
        turn_text = "Draw due to insufficient material!"
    
    status_text = font.render(turn_text, True, TEXT_COLOR)
    screen.blit(status_text, (20, HEIGHT + 20))
    
    # Draw difficulty
    diff_text = font.render(f"Difficulty: {difficulty.capitalize()}", True, TEXT_COLOR)
    screen.blit(diff_text, (WIDTH - diff_text.get_width() - 20, HEIGHT + 20))
    
    # Draw restart button
    button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT + 15, 120, 30)
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    
    button_text = font.render("New Game", True, TEXT_COLOR)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, 
                             button_rect.centery - button_text.get_height() // 2))
    
    return button_rect  # Return button rect for click detection

# Enhanced piece-square tables
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

# Improved AI evaluation
piece_values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, 
                chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}

def evaluate_board(board, difficulty):
    if board.is_checkmate():
        # Return extreme value for checkmate
        return -10000 if board.turn == chess.WHITE else 10000
    
    if board.is_stalemate() or board.is_insufficient_material():
        return 0  # Draw
        
    score = 0
    
    # Material score
    for piece_type in piece_values:
        white_pieces = len(board.pieces(piece_type, chess.WHITE))
        black_pieces = len(board.pieces(piece_type, chess.BLACK))
        score += piece_values[piece_type] * (white_pieces - black_pieces)
    
    # Position score (only for medium/hard)
    if difficulty != "easy":
        for piece_type in piece_square_tables:
            for square in board.pieces(piece_type, chess.WHITE):
                score += piece_square_tables[piece_type][square] / 10
            for square in board.pieces(piece_type, chess.BLACK):
                score -= piece_square_tables[piece_type][63 - square] / 10
    
    # Mobility (only for hard)
    if difficulty == "hard":
        # Save the current turn
        current_turn = board.turn
        
        # Calculate white mobility
        board.turn = chess.WHITE
        white_mobility = len(list(board.legal_moves))
        
        # Calculate black mobility
        board.turn = chess.BLACK
        black_mobility = len(list(board.legal_moves))
        
        # Restore the original turn
        board.turn = current_turn
        
        # Add mobility score
        score += (white_mobility - black_mobility) * 0.1
    
    return score

def alpha_beta(board, depth, alpha, beta, is_max, difficulty):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, difficulty)
    
    if is_max:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, False, difficulty)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, True, difficulty)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, difficulty):
    depth = {"easy": 2, "medium": 3, "hard": 4}[difficulty]
    randomness_factor = {"easy": 0.5, "medium": 0.2, "hard": 0.0}[difficulty]
    
    moves = list(board.legal_moves)
    if not moves:
        return None
    
    # Random move chance based on difficulty
    if random.random() < randomness_factor:
        return random.choice(moves)
    
    best_move = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    for move in moves:
        board.push(move)
        score = alpha_beta(board, depth - 1, alpha, beta, False, difficulty)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
    
    return best_move

# Promotion dialog
def get_promotion_choice():
    choices = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    images_list = ["wQ", "wR", "wB", "wN"]
    
    # Create a dialog for promotion selection
    dialog_width, dialog_height = 240, 80
    dialog_x = (WIDTH - dialog_width) // 2
    dialog_y = (HEIGHT - dialog_height) // 2
    
    running = True
    choice = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if dialog_y <= y <= dialog_y + dialog_height:
                    for i in range(4):
                        piece_x = dialog_x + i * 60 + 10
                        if piece_x <= x <= piece_x + 50:
                            choice = choices[i]
                            running = False
        
        # Draw dialog
        pygame.draw.rect(screen, pygame.Color(40, 40, 40), 
                       (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(screen, pygame.Color(200, 200, 200), 
                       (dialog_x, dialog_y, dialog_width, dialog_height), 3)
        
        # Draw pieces
        for i, img_name in enumerate(images_list):
            screen.blit(images[img_name], (dialog_x + i * 60 + 10, dialog_y + 15))
        
        font = pygame.font.SysFont("arial", 16)
        text = font.render("Choose promotion piece", True, pygame.Color(255, 255, 255))
        screen.blit(text, (dialog_x + (dialog_width - text.get_width()) // 2, dialog_y + 5))
        
        pygame.display.flip()
    
    return choice

# Select difficulty
def select_difficulty():
    font = pygame.font.SysFont("arial", 32)
    title_font = pygame.font.SysFont("arial", 42, bold=True)
    difficulties = ["easy", "medium", "hard"]
    selected = 1  # Default to medium
    
    # Create description texts
    desc_font = pygame.font.SysFont("arial", 18)
    descriptions = [
        "AI makes random moves and basic strategy.",
        "AI uses deeper search and better evaluation.",
        "AI uses advanced evaluation and deeper search."
    ]
    
    while True:
        screen.fill(pygame.Color(30, 30, 30))
        
        # Draw title
        title = title_font.render("Select AI Difficulty", True, pygame.Color(255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        
        # Draw options
        for i, diff in enumerate(difficulties):
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 + i * 80, 200, 60)
            color = BUTTON_HOVER_COLOR if i == selected else BUTTON_COLOR
            pygame.draw.rect(screen, color, button_rect, border_radius=5)
            
            # Draw button text
            text = font.render(diff.capitalize(), True, pygame.Color(255, 255, 255))
            screen.blit(text, (button_rect.centerx - text.get_width() // 2, 
                             button_rect.centery - text.get_height() // 2))
            
            # Draw description
            desc = desc_font.render(descriptions[i], True, pygame.Color(200, 200, 200))
            screen.blit(desc, (WIDTH // 2 - desc.get_width() // 2, button_rect.bottom + 5))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_RETURN:
                    return difficulties[selected]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(3):
                    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 + i * 80, 200, 60)
                    if button_rect.collidepoint(event.pos):
                        return difficulties[i]
            elif event.type == pygame.MOUSEMOTION:
                for i in range(3):
                    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 + i * 80, 200, 60)
                    if button_rect.collidepoint(event.pos):
                        selected = i

# Main game loop
def main():
    load_images()
    
    while True:
        difficulty = select_difficulty()
        board = chess.Board()
        selected_square = None
        last_move = None
        restart_button = None
        game_over = False
        running = True
        
        while running:
            # Draw game elements
            draw_board()
            draw_highlights(board, selected_square, last_move)
            draw_pieces(board)
            restart_button = draw_info_panel(board, difficulty)
            pygame.display.flip()
            
            # AI move
            if board.turn == chess.BLACK and not game_over:
                pygame.display.flip()  # Update display before AI thinks
                time.sleep(0.5)  # Small delay to make it feel more natural
                
                move = find_best_move(board, difficulty)
                if move:
                    # Play appropriate sound
                    if board.is_capture(move):
                        if CAPTURE_SOUND:
                            CAPTURE_SOUND.play()
                    else:
                        if MOVE_SOUND:
                            MOVE_SOUND.play()
                    
                    board.push(move)
                    last_move = move
                    
                    # Check if move causes check
                    if board.is_check():
                        if CHECK_SOUND:
                            CHECK_SOUND.play()
                    
                    # Check for game over after AI move
                    if board.is_game_over():
                        game_over = True
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    
                    # Check if restart button was clicked
                    if restart_button and restart_button.collidepoint(x, y):
                        running = False
                        break
                    
                    # Handle board clicks
                    if y < HEIGHT and board.turn == chess.WHITE and not game_over:
                        col = x // SQUARE_SIZE
                        row = 7 - y // SQUARE_SIZE
                        square = chess.square(col, row)
                        
                        if selected_square is None:
                            # Select a piece
                            piece = board.piece_at(square)
                            if piece and piece.color == chess.WHITE:
                                selected_square = square
                        else:
                            # Try to move the selected piece
                            move = None
                            piece = board.piece_at(selected_square)
                            
                            # Check for pawn promotion
                            if (piece and piece.piece_type == chess.PAWN and 
                                chess.square_rank(selected_square) == 6 and 
                                chess.square_rank(square) == 7):
                                # Create a temporary move for validation
                                temp_move = chess.Move(selected_square, square)
                                if any(m == temp_move or m.from_square == temp_move.from_square and 
                                      m.to_square == temp_move.to_square for m in board.legal_moves):
                                    promotion = get_promotion_choice()
                                    if promotion:
                                        move = chess.Move(selected_square, square, promotion=promotion)
                            else:
                                move = chess.Move(selected_square, square)
                            
                            # If it's a valid move, make it
                            if move and move in board.legal_moves:
                                # Play appropriate sound
                                if board.is_capture(move):
                                    if CAPTURE_SOUND:
                                        CAPTURE_SOUND.play()
                                else:
                                    if MOVE_SOUND:
                                        MOVE_SOUND.play()
                                
                                board.push(move)
                                last_move = move
                                
                                # Check if move causes check
                                if board.is_check():
                                    if CHECK_SOUND:
                                        CHECK_SOUND.play()
                                
                                # Check for game over after human move
                                if board.is_game_over():
                                    game_over = True
                            
                            selected_square = None

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
        pygame.quit()
        sys.exit(1)