from bottle import route
import json
import sqlite3
import datetime

from .processor import bot


def coordinates_of_bot(bot) -> str:
    if bot.is_moving:
        status = "bot is moving"
    else:
        status = "bot stopped"
    return json.dumps({"timestamp": datetime.datetime.utcnow().isoformat(),
                       "number": bot.number, "x": bot.x, "y": bot.y, "status": status})


@route('/coordinates')
def coordinates():
    return coordinates_of_bot(bot)


@route('/coordinates/<new_x:int>/<new_y:int>', method="POST")
def move(new_x, new_y):
    if bot.is_moving is True:
        return "Bot is already is_moving"
    else:
        bot.move_to(new_x, new_y)
        conn = sqlite3.connect(r'resources/movements.db')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM movements ORDER BY id DESC LIMIT 1""")
        last_record = cur.fetchone()
        last_id = last_record[0]
        number = last_record[1]  # need to fix, temporal solution for debugging
        new_id = last_id + 1
        new_record = (new_id, number, new_x, new_y)
        cur.execute("""INSERT INTO movements(id, number, x, y) VALUES(?, ?, ?, ?)""", new_record)
        conn.commit()
        return "movement is over"


@route('/movements')
def movements():
    conn = sqlite3.connect(r'src/resources/movements.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM movements")
    movements_raw = cur.fetchall()
    print(movements_raw)
    movements = {}
    for (id, number, x, y) in movements_raw:
        move = {"id": id, "number": number, "x": x, "y": y}
        movements[id] = move
    return json.dumps(movements)
