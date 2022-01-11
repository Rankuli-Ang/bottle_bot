import time
import sqlite3

conn = sqlite3.connect(r'resources/movements.db')
cur = conn.cursor()


class Bot:

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.moves = False

    def step_x(self, new_x: int) -> None:
        if new_x == self.x:
            return
        elif new_x < self.x:
            self.x -= 0.01
            self.x = round(self.x, 3)
            time.sleep(0.01)
        elif new_x > self.x:
            self.x += 0.01
            self.x = round(self.x, 3)
            time.sleep(0.01)

    def step_y(self, new_y: int) -> None:
        if new_y == self.y:
            return
        elif new_y < self.y:
            self.y -= 0.01
            self.y = round(self.y, 3)
            time.sleep(0.01)
        elif new_y > self.y:
            self.y += 0.01
            self.y = round(self.y, 3)
            time.sleep(0.01)

    def move_to(self, new_x: int, new_y: int):
        self.moves = True
        while self.x != new_x and self.y != new_y:
            self.step_x(new_x)
            self.step_y(new_y)
        self.moves = False

