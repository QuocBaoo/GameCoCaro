from const import BOARD_SIZE

def check_winner(board, x, y, symbol):
    """
    Kiem tra 5 quan lien tiep: Ngang, Doc, Cheo Chinh, Cheo Phu
    """
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dx, dy in directions:
        count = 1
        # Huong xuoi
        for k in range(1, 5):
            nx, ny = x + k*dx, y + k*dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == symbol:
                count += 1
            else: break
        
        # Huong nguoc
        for k in range(1, 5):
            nx, ny = x - k*dx, y - k*dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == symbol:
                count += 1
            else: break
        
        if count >= 5: return True
    return False