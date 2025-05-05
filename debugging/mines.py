#!/usr/bin/python3
import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        self.total_cells = width * height
        self.mine_indices = set(random.sample(range(self.total_cells), mines))
        self.field = [[' ' for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.mines = mines
        self.safe_cells = self.total_cells - mines
        self.revealed_count = 0

    def print_board(self, reveal=False):
        clear_screen()
        print('   ' + ' '.join(f"{i:2}" for i in range(self.width)))
        for y in range(self.height):
            print(f"{y:2} ", end='')
            for x in range(self.width):
                if reveal or self.revealed[y][x]:
                    if self.is_mine(x, y):
                        print('* ', end='')
                    else:
                        count = self.count_mines_nearby(x, y)
                        print(f"{count} " if count > 0 else '  ', end='')
                else:
                    print('. ', end='')
            print()

    def is_mine(self, x, y):
        return (y * self.width + x) in self.mine_indices

    def count_mines_nearby(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.is_mine(nx, ny):
                        count += 1
        return count

    def reveal(self, x, y):
        if self.revealed[y][x]:
            return True  # Already revealed

        if self.is_mine(x, y):
            return False

        self.revealed[y][x] = True
        self.revealed_count += 1

        if self.count_mines_nearby(x, y) == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.reveal(nx, ny)

        return True

    def play(self):
        while True:
            self.print_board()
            try:
                x = int(input("Enter x coordinate: "))
                y = int(input("Enter y coordinate: "))
                if not (0 <= x < self.width and 0 <= y < self.height):
                    print("Coordinates out of bounds.")
                    continue
                if not self.reveal(x, y):
                    self.print_board(reveal=True)
                    print("💣 Game Over! You hit a mine.")
                    break
                if self.revealed_count == self.safe_cells:
                    self.print_board(reveal=True)
                    print("🎉 Congratulations! You cleared the field.")
                    break
            except ValueError:
                print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    game = Minesweeper()
    game.play()

