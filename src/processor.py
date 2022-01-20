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

    def create_bot(self) -> None:
        """Creates new bot."""
        pass

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
        bot.target_x = target_x
        bot.target_y = target_y
        print(bot.get_target_x())
        print(bot.get_target_y())
        while bot.get_x() != bot.get_target_x() and bot.get_y() != bot.get_target_y(): # correct this
            conn = sqlite3.connect(r'resources/bots.db')
            cur = conn.cursor()
            self.bot_step_x(bot)
            self.bot_step_y(bot)
            new_coordinates = (bot.get_x(), bot.get_y())
            print(bot.get_x())
            print(bot.get_y())
            cur.execute("""UPDATE bots SET x = ?, y = ? WHERE id = ?""", new_coordinates)
            conn.commit()
            time.sleep(2)
