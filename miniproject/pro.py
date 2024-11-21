import pygame
import sys

# กำหนดขนาดหน้าต่างและสี
WIDTH, HEIGHT = 750, 750
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (50, 205, 50)

# โหลดตัวหมาก
PIECES = {
    "bk": pygame.image.load("black_king.png"),
    "bq": pygame.image.load("black_queen.png"),
    "br": pygame.image.load("black_rook.png"),
    "bb": pygame.image.load("black_bishop.png"),
    "bn": pygame.image.load("black_knight.png"),
    "bp": pygame.image.load("black_pawn.png"),
    "wk": pygame.image.load("white_king.png"),
    "wq": pygame.image.load("white_queen.png"),
    "wr": pygame.image.load("white_rook.png"),
    "wb": pygame.image.load("white_bishop.png"),
    "wn": pygame.image.load("white_knight.png"),
    "wp": pygame.image.load("white_pawn.png"),
}

# สร้างกระดานเริ่มต้น
def create_board():
    board = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["" for _ in range(COLS)],
        ["" for _ in range(COLS)],
        ["" for _ in range(COLS)],
        ["" for _ in range(COLS)],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
    ]
    return board

# วาดตารางหมากรุก
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# วาดตัวหมาก
def draw_pieces(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "":
                piece_image = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))
                win.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# ตรวจสอบการเลือกหมาก
def get_square_under_mouse(board):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row, col = mouse_y // SQUARE_SIZE, mouse_x // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None, None

def rook_moves(board, row, col):
    moves = []

    # เดินขึ้น
    for r in range(row - 1, -1, -1):
        if board[r][col] == "":
            moves.append((r, col))
        elif board[r][col][0] != board[row][col][0]:
            moves.append((r, col))
            break
        else:
            break

    # เดินลง
    for r in range(row + 1, ROWS):
        if board[r][col] == "":
            moves.append((r, col))
        elif board[r][col][0] != board[row][col][0]:
            moves.append((r, col))
            break
        else:
            break

    # เดินซ้าย
    for c in range(col - 1, -1, -1):
        if board[row][c] == "":
            moves.append((row, c))
        elif board[row][c][0] != board[row][col][0]:
            moves.append((row, c))
            break
        else:
            break

    # เดินขวา
    for c in range(col + 1, COLS):
        if board[row][c] == "":
            moves.append((row, c))
        elif board[row][c][0] != board[row][col][0]:
            moves.append((row, c))
            break
        else:
            break

    return moves

def bishop_moves(board, row, col):
    moves = []

    # เดินเฉียงในทุกทิศทาง
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # ซ้ายบน, ขวาบน, ซ้ายล่าง, ขวาล่าง
    for dr, dc in directions:
        r, c = row, col
        while True:
            r, c = r + dr, c + dc
            if 0 <= r < ROWS and 0 <= c < COLS:  # ตรวจสอบขอบเขต
                if board[r][c] == "":
                    moves.append((r, c))  # ช่องว่าง เพิ่มในลิสต์การเดิน
                elif board[r][c][0] != board[row][col][0]:
                    moves.append((r, c))  # เจอศัตรู เพิ่มและหยุด
                    break
                else:
                    break  # เจอพวกเดียวกัน หยุด
            else:
                break  # ออกนอกกระดาน

    return moves

def knight_moves(board, row, col):
    moves = []
    knight_directions = [
        (-2, -1), (-2, 1), (2, -1), (2, 1),
        (-1, -2), (-1, 2), (1, -2), (1, 2)
    ]

    for dr, dc in knight_directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == "" or board[r][c][0] != board[row][col][0]:
                moves.append((r, c))

    return moves

def king_moves(board, row, col):
    moves = []
    king_directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for dr, dc in king_directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == "" or board[r][c][0] != board[row][col][0]:
                moves.append((r, c))

    return moves

def get_valid_moves(board, selected_row, selected_col):
    piece = board[selected_row][selected_col]
    moves = []

    if piece == "wp":  # White Pawn
        if selected_row > 0 and board[selected_row - 1][selected_col] == "":
            moves.append((selected_row - 1, selected_col))
        if selected_row == 6 and board[selected_row - 2][selected_col] == "" and board[selected_row - 1][selected_col] == "":
            moves.append((selected_row - 2, selected_col))
        # การกินเบี้ย (ทะแยง)
        if selected_row > 0 and selected_col > 0 and board[selected_row - 1][selected_col - 1] != "" and board[selected_row - 1][selected_col - 1][0] != "w":
            moves.append((selected_row - 1, selected_col - 1))
        if selected_row > 0 and selected_col < COLS - 1 and board[selected_row - 1][selected_col + 1] != "" and board[selected_row - 1][selected_col + 1][0] != "w":
            moves.append((selected_row - 1, selected_col + 1))

    elif piece == "bp":  # Black Pawn
        if selected_row < ROWS - 1 and board[selected_row + 1][selected_col] == "":
            moves.append((selected_row + 1, selected_col))
        if selected_row == 1 and board[selected_row + 2][selected_col] == "" and board[selected_row + 1][selected_col] == "":
            moves.append((selected_row + 2, selected_col))
        # การกินเบี้ย (ทะแยง)
        if selected_row < ROWS - 1 and selected_col > 0 and board[selected_row + 1][selected_col - 1] != "" and board[selected_row + 1][selected_col - 1][0] != "b":
            moves.append((selected_row + 1, selected_col - 1))
        if selected_row < ROWS - 1 and selected_col < COLS - 1 and board[selected_row + 1][selected_col + 1] != "" and board[selected_row + 1][selected_col + 1][0] != "b":
            moves.append((selected_row + 1, selected_col + 1))

    elif piece[1] == "r":  # Rook
        moves = rook_moves(board, selected_row, selected_col)
    elif piece[1] == "b":  # Bishop
        moves = bishop_moves(board, selected_row, selected_col)
    elif piece[1] == "q":  # Queen
        moves = rook_moves(board, selected_row, selected_col) + bishop_moves(board, selected_row, selected_col)
    elif piece[1] == "k":  # King
        moves = king_moves(board, selected_row, selected_col)
    elif piece[1] == "n":  # Knight
        moves = knight_moves(board, selected_row, selected_col)

    return moves

def is_king_in_check(board, king_position, enemy_color):

    king_row, king_col = king_position

    # ตรวจสอบการโจมตีโดย Knight
    knight_moves = [
        (-2, -1), (-2, 1), (2, -1), (2, 1),
        (-1, -2), (-1, 2), (1, -2), (1, 2)
    ]
    for dr, dc in knight_moves:
        r, c = king_row + dr, king_col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == f"{enemy_color}n":  # Knight ของฝ่ายตรงข้าม
                return True

    # ตรวจสอบการโจมตีโดย Rook หรือ Queen (แนวตรง)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = king_row, king_col
        while 0 <= r < ROWS and 0 <= c < COLS:
            r, c = r + dr, c + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] != "":
                    if board[r][c][0] == enemy_color and (board[r][c][1] == "r" or board[r][c][1] == "q"):
                        return True
                    break

    # ตรวจสอบการโจมตีโดย Bishop หรือ Queen (แนวเฉียง)
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        r, c = king_row, king_col
        while 0 <= r < ROWS and 0 <= c < COLS:
            r, c = r + dr, c + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] != "":
                    if board[r][c][0] == enemy_color and (board[r][c][1] == "b" or board[r][c][1] == "q"):
                        return True
                    break

    # ตรวจสอบการโจมตีโดย Pawn
    pawn_directions = [(-1, -1), (-1, 1)] if enemy_color == "w" else [(1, -1), (1, 1)]
    for dr, dc in pawn_directions:
        r, c = king_row + dr, king_col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == f"{enemy_color}p":
                return True

    # ตรวจสอบการโจมตีโดย King
    king_directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    for dr, dc in king_directions:
        r, c = king_row + dr, king_col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == f"{enemy_color}k":
                return True

    return False

# ฟังก์ชันหลัก
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("เกมหมากรุก")
    
    board = create_board()
    selected_piece = None
    valid_moves = []
    
    turn = "w"  # กำหนดเริ่มต้นเป็นฝ่ายขาว (w = white)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square_under_mouse(board)
                if row is not None and col is not None:
                    if selected_piece:
                        if (row, col) in valid_moves:
                            # เมื่อเลือกหมากแล้วทำการย้าย
                            piece = board[selected_piece[0]][selected_piece[1]]
                            board[row][col] = piece  # ย้ายหมาก
                            board[selected_piece[0]][selected_piece[1]] = ""  # ลบหมากเก่า
                            selected_piece = None
                            valid_moves = []
                            # สลับฝ่าย
                            turn = "b" if turn == "w" else "w"
                        else:
                            selected_piece = None
                            valid_moves = []
                    else:
                        piece = board[row][col]
                        if piece != "" and piece[0] == turn:  # ตรวจสอบว่าเป็นฝ่ายที่กำลังเล่น
                            selected_piece = (row, col)
                            valid_moves = get_valid_moves(board, row, col)

        draw_board(win)
        
        # ไฮไลต์ช่องที่เดินได้
        if selected_piece:
            for move in valid_moves:
                pygame.draw.rect(win, HIGHLIGHT_COLOR, 
                                 (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        draw_pieces(win, board)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()