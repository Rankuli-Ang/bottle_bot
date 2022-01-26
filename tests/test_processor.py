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
        output_dict = proc.create_bot_db(DB, 10, 10)
        bot_number = output_dict.keys()[0]



        self.assertIn(new_bot, proc.bots)
        cur.execute('''SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1 ''', (new_number,))
        bot_stats = cur.fetchone()
        self.assertEqual(new_bot_data, bot_stats)

    def test_delete_bot_db(self) -> None:
        """Checks deletion bot from the database."""
        cur.execute('''SELECT * FROM bots WHERE id = 1 ORDER BY id DESC LIMIT 1 ''')
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
