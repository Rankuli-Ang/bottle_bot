from bottle import route, run, PasteServer
import json
from src.bot import Bot
import time
import sqlite3

conn = sqlite3.connect(r'resources/movements.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS movements(id INT PRIMARY KEY,x INT, y INT)""")
cur.execute("""SELECT * FROM movements ORDER BY id DESC LIMIT 1""")
coordinates = cur.fetchone()

bot = Bot(coordinates[1], coordinates[2])


@route('/coordinates')
def coordinates():
    if bot.moves:
        return json.dumps({"At the moment": time.localtime(), "bot_coordinate_x": bot.x, "bot_coordinate_y": bot.y,
                           "bot_status": "bot is moving"})
    else:
        return json.dumps({"At the moment": time.localtime(), "bot_coordinate_x": bot.x, "bot_coordinate_y": bot.y,
                           "bot_status": "bot stopped"})


@route('/coordinates/<new_x:int>/<new_y:int>', method="POST")
def move(new_x, new_y):
    if bot.moves is True:
        return "Bot is already moves"
    else:
        bot.move_to(new_x, new_y)
        conn = sqlite3.connect(r'resources/movements.db')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM movements ORDER BY id DESC LIMIT 1""")
        last_record = cur.fetchone()
        last_id = last_record[0]
        new_id = last_id + 1
        new_record = (new_id, new_x, new_y)
        cur.execute("""INSERT INTO movements(id, x, y) VALUES(?, ?, ?)""", new_record)
        conn.commit()
        return "movement is over"


@route('/movements')
def movements():
    conn = sqlite3.connect(r'resources/movements.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM movements")
    movements_raw = cur.fetchall()
    print(movements_raw)
    movements = {}
    for (id, x, y) in movements_raw:
        move = {"id": id, "x": x, "y": y}
        movements[id] = move
    return json.dumps(movements)


run(server=PasteServer, host='localhost', port=8080, debug=True)
