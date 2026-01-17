# game_logic.py
from const import BOARD_SIZE

def check_winner(board, x, y, symbol):
    """Kiểm tra 5 quân liên tiếp và trả về danh sách các ô thắng"""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        win_cells = [(x, y)]
        # Kiểm tra 2 hướng: tiến và lùi
        for k in range(1, 5):
            nx, ny = x + k*dx, y + k*dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == symbol:
                count += 1
                win_cells.append((nx, ny))
            else: break
        for k in range(1, 5):
            nx, ny = x - k*dx, y - k*dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == symbol:
                count += 1
                win_cells.append((nx, ny))
            else: break
            
        if count >= 5: return win_cells
    return None