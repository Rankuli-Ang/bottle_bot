import configparser
import unittest
import sqlite3
from src import processor
from src.bot import Bot

config = configparser.ConfigParser()
config.read('test_config.ini')
DB = config.get('DATABASE', 'test_db')
X = config.getint('MOVING_BOT', 'x')
Y = config.getint('MOVING_BOT', 'y')
TARGET_X = config.getint('MOVING_BOT', 'target_x')
TARGET_Y = config.getint('MOVING_BOT', 'target_y')


conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS bots(
    id INT PRIMARY KEY, 
    x INT, y INT, target_x INT, target_y INT
    )''')
conn.commit()

cur.execute('''DELETE FROM bots''')
conn.commit()

cur.execute('''INSERT INTO bots(id, x,y,target_x,target_y) VALUES(1, 0, 0, 0, 0)''')
conn.commit()

proc = processor.Processor(DB)
proc.add_all_bots()


class ProcessorTest(unittest.TestCase):
    """Test class for processor module."""

    def test_create_bot_db(self) -> None:
        """Checks creates bot function
        and addition to the database."""
        output_dict = proc.create_bot_db(10, 10)
        bot_number = output_dict['bot number']
        new_bot = proc.get_current_bot_instance(bot_number)
        self.assertIn(new_bot, proc.bots)

        cur.execute('''SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1 ''', (bot_number,))
        bot_stats = cur.fetchone()
        self.assertEqual(new_bot.stats, bot_stats)

    def test_move(self) -> None:
        """Checks correctness of bot movements."""
        new_bot = proc.create_bot_db(X, Y)
        bot_number = new_bot['bot number']
        cur.execute('''SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1  ''', (bot_number,))
        moving_bot_stats = cur.fetchone()
        proc.add_bot(moving_bot_stats)
        moving_bot = proc.get_current_bot_instance(moving_bot_stats[0])
        proc.bot_move(moving_bot, TARGET_X, TARGET_Y)
        control_stats = (moving_bot_stats[0], TARGET_X, TARGET_Y, TARGET_X, TARGET_Y)

        moved_bot = proc.get_current_bot_instance(moving_bot_stats[0])
        moved_bot_stats = moved_bot.stats
        self.assertEqual(moved_bot_stats, control_stats)

        cur.execute('''SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1 ''', (moving_bot_stats[0],))
        db_stats = cur.fetchone()
        self.assertEqual(db_stats, control_stats)

    def test_delete_bot_db(self) -> None:
        """Checks deletion bot from the database."""
        proc.delete_bot_db(1)
        cur.execute('''SELECT * FROM bots WHERE id = 1 ORDER BY id DESC LIMIT 1 ''')
        deleted_bot = cur.fetchone()
        self.assertIsNone(deleted_bot)
        self.assertIsNone(proc.get_current_bot_instance(1))

    def test_delete_all_bots_db(self) -> None:
        """Checks deletion all bots from the database."""
        proc.delete_all_bots_db()
        cur.execute('''SELECT * FROM bots''')
        all_data = cur.fetchall()
        self.assertEqual(all_data, [])
        self.assertEqual(proc.bots, [])


if __name__ == '__main__':
    unittest.main()
