from bottle import run, PasteServer
from src import bot, processor, routes
import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS bots(
    id INT PRIMARY KEY, 
    x INT, y INT, target_x INT, target_y INT
    )''')
    conn.commit()

    routes.proc.add_all_bots()

    run(server=PasteServer, host='localhost', port=8080, debug=True)


