from bottle import route
from src.bot import Bot
import json
from src.processor import Processor
import sqlite3
import time

processor = Processor()


@route('/bot/<bot_number:int>', method="POST")
def get_bot(bot_number):
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1  """, (bot_number,))
    bot_stats = cur.fetchone()
    if bot_stats is None:
        return json.dumps({'bot': 'is not exist'})
    processor.add_bot(bot_stats)
    current_bot = processor.get_current_bot(bot_stats[0])
    current_bot_output = {"id": current_bot.number,
                          "x": current_bot.get_x(), "y": current_bot.get_y(),
                          "status": processor.current_bot_is_moving(current_bot)}
    return json.dumps({"timestamp": time.time(), "bots": current_bot_output})


@route('/bots')
def get_bots():
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots""")
    bots_raw = cur.fetchall()
    bots_output = []
    for bot_stats in bots_raw:
        processor.add_bot(bot_stats)
        current_bot = processor.get_current_bot(bot_stats[0])
        current_bot_output = {"id": current_bot.number,
                              "x": current_bot.get_x(), "y": current_bot.get_y(),
                              "status": processor.current_bot_is_moving(current_bot)}
        bots_output.append(current_bot_output)
    return json.dumps({"timestamp": time.time(), "bots": bots_output})


@route('/move/<bot_number:int>/<target_x:int>/<target_y:int>', method="POST")
def move(bot_number, target_x, target_y):
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1  """, (bot_number,))
    bot_stats = cur.fetchone()
    if bot_stats is None:
        return json.dumps({'bot': 'is not exist'})
    processor.add_bot(bot_stats)
    current_bot = processor.get_current_bot(bot_stats[0])
    if current_bot.is_moving:
        return processor.current_bot_is_moving(current_bot)
    processor.bot_move(current_bot, target_x, target_y)
    return json.dumps({"movement": "is over"})
