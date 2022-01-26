import configparser
import unittest
import sqlite3
from src import processor
from src.bot import Bot


class TestProcessor(unittest.TestCase):
    """Test class for processor module."""

    def test_create_bot_db(self) -> None:
        """Checks creates bot function
        and addition to the database."""
        output_dict = proc.create_bot_db(DB, 10, 10)  # to add db as arg
        bot_number = output_dict['bot number']
        new_bot = proc.get_current_bot_instance(bot_number)
        self.assertIn(new_bot, proc.bots)

        cur.execute('''SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1 ''', (bot_number,))
        bot_stats = cur.fetchone()
        self.assertEqual(new_bot.stats, bot_stats)

    def test_move(self) -> None:
        target_x = 3
        target_y = 3


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
        self.assertIsNone(all_data)
        self.assertEqual(proc.bots, [])


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('src/config.ini')
    DB = config.get('DATABASE', 'test_db')

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''DELETE * FROM bots''')

    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS bots(
        id INT PRIMARY KEY, 
        x INT, y INT, target_x INT, target_y INT
        )''')
    conn.commit()
    cur.execute('''INSERT INTO bots(id, x,y,target_x,target_y) VALUES(1, 0, 0, 0, 0)''')
    conn.commit()

    proc = processor.Processor(DB)
    proc.add_all_bots()

    unittest.main()
