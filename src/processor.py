from src.bot import Bot
import sqlite3
import time


class Processor:
    """Processes movements of the bots."""

    def __init__(self):
        self.bots = []

    def add_bot(self, new_bot_stats: tuple) -> None:
        """Adds a bot to the processor list, if it not in list."""
        for bot in self.bots:
            if bot.number == new_bot_stats[0]:
                return
        new_bot = Bot(new_bot_stats[0], new_bot_stats[1], new_bot_stats[2],
                      new_bot_stats[3], new_bot_stats[4])
        self.bots.append(new_bot)

    def create_bot(self, x: int, y: int) -> dict:
        """Creates new bot."""

        conn = sqlite3.connect(r'resources/bots.db')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM bots WHERE id ORDER BY id DESC LIMIT 1  ''')
        last_bot = cur.fetchone()
        new_number = last_bot[0] + 1
        new_bot = Bot(new_number, x, y, x, y)
        new_bot_data = new_bot.stats
        print(new_bot_data)
        cur.execute('''INSERT INTO bots VALUES ?, ?, ?, ?, ?''', (new_bot_data,))
        conn.commit()
        return {new_number: 'is created'}

    def delete_bot(self, bot_number: int) -> dict:
        """Deletes bot with given number."""
        conn = sqlite3.connect(r'resources/bots.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM bots WHERE id = ?''', (bot_number,))
        return {bot_number: 'is deleted'}

    def get_current_bot(self, searched_bot_number: int):
        """Returns bot instance with a searched bot number."""

        for bot in self.bots:
            if bot.number == searched_bot_number:
                return bot

    def current_bot_is_moving(self, current_bot) -> str:
        """Returns string with a current bot moving status."""

        if current_bot.is_moving:
            return 'is moving'
        else:
            return 'stopped'

    def bot_step_x(self, bot) -> None:
        """Changes 'x' coordinate to 1 closer to target."""

        if bot.get_x() == bot.get_target_x():
            return
        elif bot.get_x() < bot.get_target_x():
            bot.x += 1
        else:
            bot.x -= 1

    def bot_step_y(self, bot) -> None:
        """Changes 'y' coordinate to 1 closer to target."""
        if bot.get_y() == bot.get_target_y():
            return
        elif bot.get_y() < bot.get_target_y():
            bot.y += 1
        else:
            bot.y -= 1

    def bot_move(self, bot, target_x: int, target_y: int) -> None:
        """Changes bot coordinates
        with 1 second sleep after every step
        and save it to the database."""
        conn = sqlite3.connect(r'resources/bots.db')
        cur = conn.cursor()
        bot.target_x = target_x
        bot.target_y = target_y
        new_targets = (bot.get_target_x(), bot.get_target_y(), bot.number)
        cur.execute("""UPDATE bots SET target_x = ?, target_y = ? WHERE id = ?""", new_targets)

        movement_is_over = False
        while movement_is_over is False:  # bad decision, but i don't come up another yet
            self.bot_step_x(bot)
            self.bot_step_y(bot)
            new_coordinates = (bot.get_x(), bot.get_y(), bot.number)
            cur.execute("""UPDATE bots SET x = ?, y = ? WHERE id = ?""", new_coordinates)
            conn.commit()
            time.sleep(1)
            if bot.get_x() == bot.get_target_x() and bot.get_y() == bot.get_target_y():
                return
