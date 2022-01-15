import time


class Bot:

    def __init__(self, number: int, x: int, y: int):
        self.number = number
        self.x: int = x
        self.y: int = y
        self.target_x = None
        self.target_y = None
        self.is_moving = False

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
        self.is_moving = True
        while self.x != new_x and self.y != new_y:
            self.step_x(new_x)
            self.step_y(new_y)
        self.is_moving = False

    def set_target(self, target_x: int, target_y: int) -> None:
        self.target_x = target_x
        self.target_y = target_y
