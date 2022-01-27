from src.bot import Bot
import sqlite3
import time


class Processor:
    """Processes movements of the bots."""

    def __init__(self, db):
        self.db = db
        self.bots = []

    def add_bot(self, new_bot_stats: tuple) -> None:
        """Adds a bot to the proc list, if it not in list."""
        for bot in self.bots:
            if bot.get_number() == new_bot_stats[0]:
                return
        new_bot = Bot(new_bot_stats[0], new_bot_stats[1], new_bot_stats[2],
                      new_bot_stats[3], new_bot_stats[4])
        self.bots.append(new_bot)

    def add_all_bots(self) -> None:
        """Adds all bot to the proc's list."""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM bots''')
        all_bots_stats = cur.fetchall()
        for bot_stats in all_bots_stats:
            self.add_bot(bot_stats)

    def delete_bot(self, delete_bot_number: int) -> None:
        """Deletes bot from the proc list."""
        delete_bot = None
        for bot in self.bots:
            if bot.get_number() == delete_bot_number:
                delete_bot = bot
                break
        if delete_bot is None:
            return
        self.bots.remove(delete_bot)

    def create_bot_db(self, x: int, y: int) -> dict:
        """Creates new bot."""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM bots WHERE id ORDER BY id DESC LIMIT 1  ''')
        last_bot = cur.fetchone()
        if last_bot is not None:
            new_number = last_bot[0] + 1
        else:
            new_number = 1
        new_bot = Bot(new_number, x, y, x, y)
        new_bot_data = new_bot.stats
        self.add_bot(new_bot_data)
        cur.execute('''INSERT INTO bots(id, x,y,target_x,target_y) VALUES(?,?,?,?,?)''', new_bot_data)
        conn.commit()
        return {'bot': 'is created', 'bot number': new_number}

    def delete_bot_db(self, bot_number: int) -> dict:
        """Deletes bot with given number."""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1 ''', (bot_number,))
        deleting_bot_stats = cur.fetchone()
        if not deleting_bot_stats:
            return {'bot': 'does not exists'}
        deleting_bot = self.get_current_bot_instance(bot_number)
        if deleting_bot.is_moving:
            return {'ERROR': 'You cannot bot while its moving'}
        self.delete_bot(bot_number)
        cur.execute('''DELETE FROM bots WHERE id = ?''', (bot_number,))
        conn.commit()
        return {bot_number: 'is deleted'}

    def delete_all_bots_db(self) -> dict:
        """Deletes all bots from the database."""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        for bot in self.bots:
            if bot.is_moving:
                return {'ERROR': 'You cannot delete all bots, while at least one moving'}
        self.bots.clear()
        cur.execute('''DELETE from bots''')
        conn.commit()
        return {'list of bots': 'is empty'}

    def get_current_bot_instance(self, searched_bot_number: int):
        """Returns bot instance with a searched bot number."""
        for bot in self.bots:
            if bot.get_number() == searched_bot_number:
                return bot

    def current_bot_stats(self, bot) -> dict:
        """Returns current bot stats."""
        return {'id': bot.stats[0],
                'x': bot.stats[1], 'y': bot.stats[2],
                'status': self.current_bot_is_moving(bot)}

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
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        bot.target_x = target_x
        bot.target_y = target_y
        new_targets = (bot.get_target_x(), bot.get_target_y(), bot.get_number())
        cur.execute("""UPDATE bots SET target_x = ?, target_y = ? WHERE id = ?""", new_targets)

        while not bot.get_x() == bot.get_target_x() and not bot.get_y() == bot.get_target_y():
            self.bot_step_x(bot)
            self.bot_step_y(bot)
            new_coordinates = (bot.get_x(), bot.get_y(), bot.get_number())
            cur.execute("""UPDATE bots SET x = ?, y = ? WHERE id = ?""", new_coordinates)
            conn.commit()
            time.sleep(1)

