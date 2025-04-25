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

# Cải thiện đánh giá nước đi cho việc sắp xếp
def evaluate_move(board, move):
    score = 0
    
    # Ưu tiên nước ăn quân
    if board.is_capture(move):
        victim_piece = board.piece_at(move.to_square)
        attacker_piece = board.piece_at(move.from_square)
        if victim_piece and attacker_piece:
            # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
            score += 10 * piece_values.get(victim_piece.piece_type, 0) - piece_values.get(attacker_piece.piece_type, 0) / 10
    
    # Ưu tiên phong tốt
    if move.promotion:
        score += 900
    
    # Ưu tiên nước chiếu
    board.push(move)
    if board.is_check():
        score += 50
    board.pop()
    
    # Ưu tiên các nước đi vào trung tâm cho quân tốt và mã
    piece = board.piece_at(move.from_square)
    if piece:
        if piece.piece_type == chess.PAWN or piece.piece_type == chess.KNIGHT:
            to_file = chess.square_file(move.to_square)
            to_rank = chess.square_rank(move.to_square)
            # Điểm cho ô ở gần trung tâm
            center_distance = abs(3.5 - to_file) + abs(3.5 - to_rank)
            score += (4 - center_distance) * 5
    
    return score

# Improved board evaluation
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
            # Special handling for king in endgame
            if piece_type == chess.KING and len(list(board.piece_map().keys())) <= 12:
                # Endgame - use endgame king table
                for square in board.pieces(piece_type, chess.WHITE):
                    score += king_endgame_table[square] / 10
                for square in board.pieces(piece_type, chess.BLACK):
                    score -= king_endgame_table[63 - square] / 10
            else:
                # Normal piece square tables
                for square in board.pieces(piece_type, chess.WHITE):
                    score += piece_square_tables[piece_type][square] / 10
                for square in board.pieces(piece_type, chess.BLACK):
                    score -= piece_square_tables[piece_type][63 - square] / 10
    
    # Chỉ áp dụng các đánh giá nâng cao cho chế độ khó
    if difficulty == "hard":
        # Tính điểm di động quân
        current_turn = board.turn
        
        # Đánh giá di động của trắng
        board.turn = chess.WHITE
        white_mobility = len(list(board.legal_moves))
        
        # Đánh giá di động của đen
        board.turn = chess.BLACK
        black_mobility = len(list(board.legal_moves))
        
        # Khôi phục lượt đi ban đầu
        board.turn = current_turn
        
        # Thêm điểm di động
        score += (white_mobility - black_mobility) * 0.1
        
        # Đánh giá an toàn của vua
        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)
        
        # Khuyến khích nhập thành cho vua
        if white_king_square in [chess.G1, chess.C1]:
            score += 30
        if black_king_square in [chess.G8, chess.C8]:
            score -= 30
        
        # Đánh giá kiểm soát trung tâm
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        for square in center_squares:
            # Kiểm tra quân kiểm soát hoặc chiếm giữ ô trung tâm
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    score += 10
                else:
                    score -= 10
            
            # Kiểm tra tốt kiểm soát trung tâm
            for pawn_square in board.pieces(chess.PAWN, chess.WHITE):
                pawn_file = chess.square_file(pawn_square)
                pawn_rank = chess.square_rank(pawn_square)
                
                # Xem xét các ô tốt kiểm soát
                if 2 <= pawn_file <= 5 and 3 <= pawn_rank <= 4:
                    score += 5
            
            for pawn_square in board.pieces(chess.PAWN, chess.BLACK):
                pawn_file = chess.square_file(pawn_square)
                pawn_rank = chess.square_rank(pawn_square)
                
                if 2 <= pawn_file <= 5 and 3 <= pawn_rank <= 4:
                    score -= 5
        
        # Phát triển quân sớm trong giai đoạn đầu
        if len(list(board.piece_map().keys())) > 28:  # Giai đoạn đầu trận
            # Khuyến khích phát triển quân sớm
            developed_white = 0
            developed_black = 0
            
            # Kiểm tra mã và tượng đã di chuyển chưa
            if not board.piece_at(chess.B1) or board.piece_at(chess.B1).piece_type != chess.KNIGHT:
                developed_white += 1
            if not board.piece_at(chess.G1) or board.piece_at(chess.G1).piece_type != chess.KNIGHT:
                developed_white += 1
            if not board.piece_at(chess.C1) or board.piece_at(chess.C1).piece_type != chess.BISHOP:
                developed_white += 1
            if not board.piece_at(chess.F1) or board.piece_at(chess.F1).piece_type != chess.BISHOP:
                developed_white += 1
                
            if not board.piece_at(chess.B8) or board.piece_at(chess.B8).piece_type != chess.KNIGHT:
                developed_black += 1
            if not board.piece_at(chess.G8) or board.piece_at(chess.G8).piece_type != chess.KNIGHT:
                developed_black += 1
            if not board.piece_at(chess.C8) or board.piece_at(chess.C8).piece_type != chess.BISHOP:
                developed_black += 1
            if not board.piece_at(chess.F8) or board.piece_at(chess.F8).piece_type != chess.BISHOP:
                developed_black += 1
            
            score += developed_white * 10
            score -= developed_black * 10
    
    return score

# Alpha-Beta with memory (transposition table)
def alpha_beta_with_memory(board, depth, alpha, beta, is_max, difficulty):
    # Tạo khóa băm cho vị trí
    board_hash = board.fen()
    
    # Kiểm tra nếu vị trí đã được đánh giá trước đó
    if board_hash in transposition_table and transposition_table[board_hash]["depth"] >= depth:
        return transposition_table[board_hash]["score"]
    
    if depth == 0 or board.is_game_over():
        score = evaluate_board(board, difficulty)
        # Lưu vào bảng
        transposition_table[board_hash] = {"score": score, "depth": depth}
        return score
    
    if is_max:
        max_eval = float('-inf')
        
        # Sắp xếp nước đi để tối ưu cắt tỉa
        moves = list(board.legal_moves)
        move_scores = []
        for move in moves:
            move_scores.append((move, evaluate_move(board, move)))
        
        # Sắp xếp nước đi từ tốt nhất đến kém nhất cho max
        sorted_moves = [move for move, score in sorted(move_scores, key=lambda x: -x[1])]
        
        for move in sorted_moves:
            board.push(move)
            eval = alpha_beta_with_memory(board, depth - 1, alpha, beta, False, difficulty)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        # Lưu vào bảng
        transposition_table[board_hash] = {"score": max_eval, "depth": depth}
        return max_eval
    else:
        min_eval = float('inf')
        
        # Sắp xếp nước đi để tối ưu cắt tỉa
        moves = list(board.legal_moves)
        move_scores = []
        for move in moves:
            move_scores.append((move, evaluate_move(board, move)))
        
        # Sắp xếp nước đi từ tốt nhất đến kém nhất cho min
        sorted_moves = [move for move, score in sorted(move_scores, key=lambda x: x[1])]
        
        for move in sorted_moves:
            board.push(move)
            eval = alpha_beta_with_memory(board, depth - 1, alpha, beta, True, difficulty)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        
        # Lưu vào bảng
        transposition_table[board_hash] = {"score": min_eval, "depth": depth}
        return min_eval

# Quiescence search to avoid horizon effect
def alpha_beta_quiescence(board, depth, alpha, beta, q_alpha, q_beta, difficulty):
    # Đánh giá hiện tại
    stand_pat = evaluate_board(board, difficulty)
    
    # Beta cutoff
    if stand_pat >= beta:
        return beta
    
    # Update alpha if needed
    if stand_pat > alpha:
        alpha = stand_pat
    
    # If reached max depth but position is not quiet, continue searching
    if depth <= 0:
        # Only consider captures and promotions
        for move in board.legal_moves:
            if board.is_capture(move) or move.promotion:
                board.push(move)
                score = -alpha_beta_quiescence(board, -1, -q_beta, -q_alpha, -q_beta, -q_alpha, difficulty)
                board.pop()
                
                if score >= q_beta:
                    return q_beta
                if score > q_alpha:
                    q_alpha = score
        return q_alpha
    
    # Normal search
    for move in board.legal_moves:
        board.push(move)
        score = -alpha_beta_quiescence(board, depth - 1, -beta, -alpha, -beta, -alpha, difficulty)
        board.pop()
        
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    return alpha

# Find best move at specified depth
def find_best_move_at_depth(board, difficulty, depth):
    global transposition_table
    
    moves = list(board.legal_moves)
    if not moves:
        return None
    
    move_scores = []
    alpha = float('-inf')
    beta = float('inf')
    
    # Đánh giá tất cả nước đi hợp lệ
    for move in moves:
        board.push(move)
        score = -alpha_beta_with_memory(board, depth - 1, -beta, -alpha, True, difficulty)
        board.pop()
        move_scores.append((move, score))
        alpha = max(alpha, score)
    
    # Sắp xếp nước đi theo điểm số
    best_moves = sorted(move_scores, key=lambda x: x[1], reverse=True)
    
    if best_moves:
        return best_moves[0][0]
    return None

# Find best move with timeout
def find_best_move_with_timeout(board, difficulty, max_time=3.0):
    start_time = time.time()
    
    # Đối với chế độ khó, bắt đầu với độ sâu thấp và tăng lên
    if difficulty == "hard":
        current_depth = 2
        max_depth = 4
        best_move = None
        
        while current_depth <= max_depth:
            # Nếu quá thời gian, trả về nước đi tốt nhất tìm được trước đó
            if time.time() - start_time > max_time and best_move:
                return best_move
            
            move = find_best_move_at_depth(board, difficulty, current_depth)
            if move:
                best_move = move
            
            current_depth += 1
            
            # Nếu đã hết thời gian, dừng tìm kiếm
            if time.time() - start_time > max_time:
                break
                
        return best_move if best_move else find_best_move_at_depth(board, difficulty, 2)
    else:
        # Chế độ dễ và trung bình sử dụng phương thức thông thường
        return find_best_move(board, difficulty)

# Find best move
def find_best_move(board, difficulty):
    global transposition_table
    # Xóa bảng đệm cho mỗi lượt mới để tránh sử dụng quá nhiều bộ nhớ
    transposition_table = {}
    
    # Độ sâu tìm kiếm dựa trên độ khó
    depth = {"easy": 2, "medium": 3, "hard": 4}[difficulty]
    randomness_factor = {"easy": 0.5, "medium": 0.2, "hard": 0.0}[difficulty]
    
    moves = list(board.legal_moves)
    if not moves:
        return None
    
    # Di chuyển ngẫu nhiên dựa vào độ khó
    if random.random() < randomness_factor:
        return random.choice(moves)
    
    # Thêm tìm kiếm quiesce cho chế độ khó
    use_quiescence = (difficulty == "hard")
    
    # Tối ưu: chỉ đánh giá nước đi tốt hơn ở mức cao nhất
    move_scores = []
    alpha = float('-inf')
    beta = float('inf')
    
    # Đánh giá tất cả nước đi hợp lệ
    for move in moves:
        board.push(move)
        # Nếu là chế độ khó, dùng tìm kiếm quiesce
        if use_quiescence:
            score = -alpha_beta_quiescence(board, depth - 1, -beta, -alpha, -float('inf'), float('inf'), difficulty)
        else:
            score = -alpha_beta_with_memory(board, depth - 1, -beta, -alpha, False, difficulty)
        board.pop()
        move_scores.append((move, score))
        alpha = max(alpha, score)
    
    # Sắp xếp các nước đi theo điểm và trả về nước đi tốt nhất
    best_moves = sorted(move_scores, key=lambda x: x[1], reverse=True)
    
    # Nếu chế độ khó, luôn chọn nước đi tốt nhất
    if difficulty == "hard":
        return best_moves[0][0]
    else:
        # Chọn trong top nước đi tốt nhất để tăng tính ngẫu nhiên
        # Chọn trong top 3 nước đi cho trung bình, top 5 cho dễ
        top_n = 3 if difficulty == "medium" else 5
        top_n = min(top_n, len(best_moves))
        return random.choice([move for move, _ in best_moves[:top_n]])

def main():
    # Initialize the game
    board = chess.Board()
    selected_square = None
    last_move = None
    running = True
    game_over = False
    difficulty = "medium"  # Default difficulty
    
    # Load images
    load_images()
    
    while running:
        # Draw the board and pieces
        draw_board()
        draw_pieces(board)
        draw_highlights(board, selected_square, last_move)
        restart_button = draw_info_panel(board, difficulty)
        pygame.display.flip()
        
        # Check if game is over
        if board.is_game_over() and not game_over:
            game_over = True
            if MOVE_SOUND:  # Play appropriate sound for checkmate
                if board.is_checkmate():
                    CHECK_SOUND.play()
        
        # If it's AI's turn and game is not over
        if board.turn == chess.BLACK and not game_over:
            # Show thinking message by redrawing the info panel
            draw_info_panel(board, difficulty)
            pygame.display.flip()
            
            # Find and make the AI move
            ai_move = find_best_move_with_timeout(board, difficulty)
            if ai_move:
                # Play appropriate sound
                if board.is_capture(ai_move):
                    if CAPTURE_SOUND:
                        CAPTURE_SOUND.play()
                elif ai_move.from_square in [chess.E1, chess.E8] and chess.square_file(ai_move.to_square) in [2, 6]:
                    if CASTLE_SOUND:
                        CASTLE_SOUND.play()
                elif MOVE_SOUND:
                    MOVE_SOUND.play()
                
                board.push(ai_move)
                last_move = ai_move
                
                # Check if the move results in check
                if board.is_check() and CHECK_SOUND:
                    CHECK_SOUND.play()
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Check if restart button was clicked
                if restart_button.collidepoint(x, y):
                    board = chess.Board()
                    selected_square = None
                    last_move = None
                    game_over = False
                    continue
                
                # Process board clicks only if it's human's turn and game is not over
                if board.turn == chess.WHITE and not game_over and y < HEIGHT:
                    file = x // SQUARE_SIZE
                    rank = 7 - (y // SQUARE_SIZE)
                    square = chess.square(file, rank)
                    
                    # If a square is already selected, try to make a move
                    if selected_square is not None:
                        move = chess.Move(selected_square, square)
                        # Check for promotion
                        if board.piece_at(selected_square) and board.piece_at(selected_square).piece_type == chess.PAWN:
                            if rank == 7 or rank == 0:  # Promotion rank
                                move.promotion = chess.QUEEN  # Default to queen promotion
                        
                        # Try to make the move
                        if move in board.legal_moves:
                            # Play appropriate sound
                            if board.is_capture(move):
                                if CAPTURE_SOUND:
                                    CAPTURE_SOUND.play()
                            elif move.from_square in [chess.E1, chess.E8] and chess.square_file(move.to_square) in [2, 6]:
                                if CASTLE_SOUND:
                                    CASTLE_SOUND.play()
                            elif MOVE_SOUND:
                                MOVE_SOUND.play()
                            
                            board.push(move)
                            last_move = move
                            selected_square = None
                            
                            # Check if the move results in check
                            if board.is_check() and CHECK_SOUND:
                                CHECK_SOUND.play()
                        else:
                            # If the move is not valid, check if clicking on own piece to select it
                            piece = board.piece_at(square)
                            if piece and piece.color == board.turn:
                                selected_square = square
                            else:
                                selected_square = None
                    else:
                        # No square selected yet, select if clicking on own piece
                        piece = board.piece_at(square)
                        if piece and piece.color == board.turn:
                            selected_square = square
            
            # Handle keyboard input for difficulty change
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_e:
                    difficulty = "easy"
                elif event.key == pygame.K_2 or event.key == pygame.K_m:
                    difficulty = "medium"
                elif event.key == pygame.K_3 or event.key == pygame.K_h:
                    difficulty = "hard"
        
        # Limit frame rate
        pygame.time.Clock().tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()