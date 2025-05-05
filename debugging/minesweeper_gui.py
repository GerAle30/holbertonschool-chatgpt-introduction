import tkinter as tk
from tkinter import messagebox
import random

class Cell(tk.Button):
    def __init__(self, master, x, y, callback, *args, **kwargs):
        super().__init__(master, width=3, height=1, font=('Arial', 14), *args, **kwargs)
        self.x = x
        self.y = y
        self.callback = callback
        self.revealed = False
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.callback(self.x, self.y)

    def reveal(self, text='', color='black'):
        if not self.revealed:
            self.revealed = True
            self.config(text=text, state='disabled', disabledforeground=color, relief='sunken')

class MinesweeperGUI:
    def __init__(self, root, width=10, height=10, mines=10):
        self.root = root
        self.width = width
        self.height = height
        self.mines = mines
        self.buttons = {}
        self.mines_positions = set(random.sample(range(width * height), mines))
        self.revealed_count = 0

        self.setup_board()

    def setup_board(self):
        for y in range(self.height):
            for x in range(self.width):
                btn = Cell(self.root, x, y, self.reveal_cell)
                btn.grid(row=y, column=x)
                self.buttons[(x, y)] = btn

    def is_mine(self, x, y):
        return y * self.width + x in self.mines_positions

    def count_mines_nearby(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if (dx != 0 or dy != 0) and (0 <= nx < self.width and 0 <= ny < self.height):
                    if self.is_mine(nx, ny):
                        count += 1
        return count

    def reveal_cell(self, x, y):
        cell = self.buttons[(x, y)]
        if cell.revealed:
            return

        if self.is_mine(x, y):
            cell.reveal('*', 'red')
            self.reveal_all_mines()
            messagebox.showerror("Game Over", "💣 You hit a mine!")
            self.disable_all()
            return

        self.flood_fill(x, y)

        if self.revealed_count == (self.width * self.height - self.mines):
            messagebox.showinfo("Congratulations!", "🎉 You cleared the minefield!")
            self.disable_all()

    def flood_fill(self, x, y):
        stack = [(x, y)]
        visited = set()

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited or self.is_mine(cx, cy):
                continue

            visited.add((cx, cy))
            cell = self.buttons[(cx, cy)]
            if not cell.revealed:
                count = self.count_mines_nearby(cx, cy)
                color = 'blue' if count > 0 else 'black'
                cell.reveal(str(count) if count > 0 else '', color)
                self.revealed_count += 1

                if count == 0:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                stack.append((nx, ny))

    def reveal_all_mines(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.is_mine(x, y):
                    self.buttons[(x, y)].reveal('*', 'red')

    def disable_all(self):
        for cell in self.buttons.values():
            cell.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = MinesweeperGUI(root, width=10, height=10, mines=10)
    root.mainloop()

