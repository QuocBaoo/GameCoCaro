# client.py
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import socket, threading, json, queue
from const import *
from game_logic import check_winner

class CaroModern:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Caro Modern Pro - 27x27")
        self.root.configure(bg=COLOR["bg"])

        self.root.withdraw()
        self.player_name = simpledialog.askstring("Tên", "Nhập tên của bạn:") or "Player"
        self.root.deiconify()

        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.my_turn = False; self.my_symbol = ""; self.opp_name = ""
        self.msg_queue = queue.Queue()

        self.setup_ui()
        self.setup_network()
        self.root.after(100, self.process_msgs)
        self.root.mainloop()

    def setup_ui(self):
        # Sidebar
        side = tk.Frame(self.root, width=300, bg=COLOR["bg"])
        side.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Hiển thị Tên và Lượt đi [Yêu cầu của bạn]
        self.lbl_me = tk.Label(side, text=f"Bạn: {self.player_name}", bg=COLOR["bg"], fg="#333333", font=("Arial", 12, "bold"))
        self.lbl_me.pack(pady=(20, 5))
        
        self.lbl_status = tk.Label(side, text="Chờ đối thủ...", bg=COLOR["bg"], fg="#555555", font=("Arial", 11, "italic"))
        self.lbl_status.pack(pady=5)

        self.lbl_score = tk.Label(side, text="Tỉ số: 0 - 0", bg=COLOR["bg"], fg="#333333", font=("Arial", 14, "bold"))
        self.lbl_score.pack(pady=20)

        self.chat_display = scrolledtext.ScrolledText(side, width=30, height=20, bg=COLOR["board"], fg=COLOR["text"], state='disabled')
        self.chat_display.pack(padx=10)
        
        self.chat_entry = tk.Entry(side, bg=COLOR["board"], fg=COLOR["text"])
        self.chat_entry.pack(fill=tk.X, padx=10, pady=10)
        self.chat_entry.bind("<Return>", self.send_chat)

        # Bàn cờ với Scrollbar
        self.canvas = tk.Canvas(self.root, width=750, height=750, bg=COLOR["board"], highlightthickness=0,
                                scrollregion=(0,0, BOARD_SIZE*UI_SIZE, BOARD_SIZE*UI_SIZE))
        sy = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        sx = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.config(yscrollcommand=sy.set, xscrollcommand=sx.set)
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)
        sy.pack(side=tk.LEFT, fill=tk.Y); sx.pack(side=tk.BOTTOM, fill=tk.X)

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_grid(self):
        for i in range(BOARD_SIZE + 1):
            self.canvas.create_line(i*UI_SIZE, 0, i*UI_SIZE, BOARD_SIZE*UI_SIZE, fill=COLOR["grid"])
            self.canvas.create_line(0, i*UI_SIZE, BOARD_SIZE*UI_SIZE, i*UI_SIZE, fill=COLOR["grid"])

    def update_turn_ui(self):
        """Cập nhật trạng thái lượt đi lên màn hình"""
        if self.my_turn:
            self.lbl_status.config(text="ĐẾN LƯỢT BẠN!", fg="#28c840")
            self.root.title(f"Lượt của {self.player_name}")
        else:
            self.lbl_status.config(text=f"Đợi {self.opp_name}...", fg="#ff5f56")
            self.root.title(f"Đợi {self.opp_name}...")

    def on_click(self, event):
        if not self.my_turn: return
        rx, ry = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        x, y = int(rx // UI_SIZE), int(ry // UI_SIZE)
        
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[y][x] == "":
            self.draw_piece(x, y, self.my_symbol)
            self.send({"type": MSG_MOVE, "x": x, "y": y, "symbol": self.my_symbol})
            if check_winner(self.board, x, y, self.my_symbol):
                self.my_turn = False
                self.send({"type": MSG_WIN})
            else:
                self.my_turn = False
                self.update_turn_ui()

    def draw_piece(self, x, y, sym):
        self.board[y][x] = sym
        color = COLOR["x"] if sym == "X" else COLOR["o"]
        m = 8
        if sym == "X":
            self.canvas.create_line(x*UI_SIZE+m, y*UI_SIZE+m, (x+1)*UI_SIZE-m, (y+1)*UI_SIZE-m, fill=color, width=3)
            self.canvas.create_line((x+1)*UI_SIZE-m, y*UI_SIZE+m, x*UI_SIZE+m, (y+1)*UI_SIZE-m, fill=color, width=3)
        else:
            self.canvas.create_oval(x*UI_SIZE+m, y*UI_SIZE+m, (x+1)*UI_SIZE-m, (y+1)*UI_SIZE-m, outline=color, width=3)

    def process_msgs(self):
        try:
            while True:
                m = self.msg_queue.get_nowait()
                if m['type'] == MSG_START:
                    # Reset ván mới
                    self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                    self.canvas.delete("all"); self.draw_grid()
                    self.my_symbol, self.my_turn = m['symbol'], m['turn']
                    self.opp_name = m.get('opp_name', 'Đối thủ')
                    self.lbl_score.config(text=f"Tỉ số: {m['s1']} - {m['s2']}")
                    self.update_turn_ui()
                elif m['type'] == MSG_MOVE:
                    self.draw_piece(m['x'], m['y'], m['symbol'])
                    self.my_turn = True; self.update_turn_ui()
                elif m['type'] == MSG_CHAT:
                    self.log(m['content'])
        except queue.Empty: pass
        self.root.after(100, self.process_msgs)

    def log(self, msg):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, msg + "\n")
        self.chat_display.config(state='disabled'); self.chat_display.see(tk.END)

    def send_chat(self, event):
        txt = self.chat_entry.get()
        if txt:
            self.send({"type": MSG_CHAT, "content": f"{self.player_name}: {txt}"})
            self.log(f"Bạn: {txt}"); self.chat_entry.delete(0, tk.END)

    def setup_network(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((HOST, PORT))
            self.send({"type": MSG_LOGIN, "name": self.player_name})
            threading.Thread(target=self.recv_loop, daemon=True).start()
        except: messagebox.showerror("Lỗi", "Không kết nối được server")

    def recv_loop(self):
        buf = ""
        while True:
            try:
                data = self.s.recv(BUFF_SIZE).decode(FORMAT)
                if not data: break
                buf += data
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    self.msg_queue.put(json.loads(line))
            except: break

    def send(self, data):
        try: self.s.send((json.dumps(data) + "\n").encode(FORMAT))
        except: pass

if __name__ == "__main__":
    CaroModern()