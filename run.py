from bottle import run, PasteServer
import configparser
from src import bot, processor, routes
import sqlite3

config = configparser.ConfigParser()
config.read("src/config.ini")
DB = config.get('DATABASE', 'db')


if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS bots(
    id INT PRIMARY KEY, 
    x INT, y INT, target_x INT, target_y INT
    )''')
    conn.commit()

    routes.proc.add_all_bots_to_proc()

    run(server=PasteServer, host='localhost', port=8080, debug=True)


