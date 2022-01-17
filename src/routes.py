from bottle import route
import json
import sqlite3
import datetime
import time


def get_bots() -> str:
    conn = sqlite3.connect(r'src/resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots""")
    bots_raw = cur.fetchall()
    bots_output = []
    for bot in bots_raw:
        id = bot[0]
        x = bot[1]
        y = bot[2]
        status = bot[3]
        bot_output = {"id": id, "x": x, "y": y, "status": status}
        bots_output.append(bot_output)
    return json.dumps({"timestamp": int(time.time()), "bots": bots_output})


@route('/bots')
def bots():
    return get_bots()


@route('/<bot: int>/<new_x:int>/<new_y:int>', method="POST")
def move(bot, new_x, new_y):
    conn = sqlite3.connect(r'src/resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots""")
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
