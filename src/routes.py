from bottle import route
import json
import sqlite3
import time


def get_bots() -> str:
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots""")
    bots_raw = cur.fetchall()
    bots_output = []
    for bot in bots_raw:
        id = bot[0]
        x = bot[1]
        y = bot[2]
        if bot[1] == bot[3] and bot[2] == bot[4]:  # change it later
            status = 'stopped'
        else:
            status = 'is moving'
        bot_output = {"id": id, "x": x, "y": y, "status": status}
        bots_output.append(bot_output)
    return json.dumps({"timestamp": int(time.time()), "bots": bots_output})  # how to correct this


@route('/bots')
def bots():
    return get_bots()


@route('/move/<bot_number:int>/<new_x:int>/<new_y:int>', method="POST")
def move(bot_number, new_x, new_y):
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots ORDER BY id DESC LIMIT 1 WHERE id = ? """, bot_number)
    bot = cur.fetchone()
    print(bot)
    data = (new_x, new_y, new_x, new_y, bot_number)
    cur.execute("""UPDATE bots SET (x = ?, y = ?, target_x = ?, target_y = ?), WHERE id = ?""", data)
    conn.commit()

