# const.py
HOST = 'localhost'
PORT = 65432
BUFF_SIZE = 4096
FORMAT = 'utf-8'

BOARD_SIZE = 40         # Mở rộng từ 24 lên 27 ô
UI_SIZE = 30            # Kích thước ô cờ
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 850

MSG_LOGIN = "LOGIN"; MSG_WAIT = "WAIT"; MSG_START = "START"
MSG_MOVE = "MOVE"; MSG_CHAT = "CHAT"; MSG_WIN = "WIN"
MSG_LOSE = "LOSE"; MSG_DISCONNECT = "DISCONNECT"

COLOR = {
    "bg": "#f0f0f0", "board": "#f0f0f0", "text": "#333333",
    "grid": "#77B3BB", "x": "#ff5f56", "o": "#28c840"
}