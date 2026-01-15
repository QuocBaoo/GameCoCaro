import tkinter as tk
from const import *

class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Giao dien Game Caro")
        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="#ffddb3")
        self.canvas.pack()
        self.draw_grid()
        self.root.mainloop()

    def draw_grid(self):
        for i in range(BOARD_SIZE):
            self.canvas.create_line(i * UI_SIZE, 0, i * UI_SIZE, WINDOW_HEIGHT)
            self.canvas.create_line(0, i * UI_SIZE, WINDOW_WIDTH, i * UI_SIZE)

if __name__ == "__main__":
    GameUI()