from bottle import route
import configparser
import json
from src.processor import Processor
import sqlite3
import time

proc = Processor()  # It's not good to create proc here, but I can't come up better decision


@route('/')
def get_tutorial():
    """Displays all commands."""
    data = {"commands": [
        {'bot/bot_number': 'returns bot statistics'},
        {'bots': 'returns statistics for all bots'},
        {'/move/bot_number/target_x/target_y': 'moves bot with a given values'},
        {'create/x/y': 'creates bot with a given values'},
        {'delete/bot_number': 'deletes bot with a given number'},
        {'delete_all': 'deletes all bots (only if everyone is stopped)'}]}
    return json.dumps(data)


@route('/bot/<bot_number:int>', method="POST")
def get_bot(bot_number):
    """Display bot stat with given number."""
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1  """, (bot_number,))
    bot_stats = cur.fetchone()
    if bot_stats is None:
        return json.dumps({'bot': 'is not exist'})
    current_bot = proc.get_current_bot_instance(bot_stats[0])
    current_bot_output = proc.current_bot_stats(current_bot)
    return json.dumps({"timestamp": time.time(), "bot": current_bot_output})


@route('/bots')
def get_bots():  # should I unite get_bot and get_bots to one function?
    """Displays stat for all bots."""
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots""")
    bots_raw = cur.fetchall()
    if not bots_raw:
        return json.dumps({"timestamp": time.time(), 'list of bots': 'is empty'})
    bots_output = []
    for bot_stats in bots_raw:
        current_bot = proc.get_current_bot_instance(bot_stats[0])
        current_bot_output = proc.current_bot_stats(current_bot)
        bots_output.append(current_bot_output)
    return json.dumps({"timestamp": time.time(), "bots": bots_output})


@route('/move/<bot_number:int>/<target_x:int>/<target_y:int>', method="POST")
def move(bot_number, target_x, target_y):
    """Moves bot with a given values."""
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1  """, (bot_number,))
    bot_stats = cur.fetchone()
    if bot_stats is None:
        return json.dumps({'bot': 'is not exist'})
    proc.add_bot(bot_stats)
    current_bot = proc.get_current_bot_instance(bot_stats[0])
    if current_bot.is_moving:
        return json.dumps({'bot': proc.current_bot_is_moving(current_bot)})
    proc.bot_move(current_bot, target_x, target_y)
    return json.dumps({"movement": "is over"})


@route('/create/<x:int>/<y:int>', method='POST')
def create_bot(x, y):
    return json.dumps(proc.create_bot_db(x, y))


@route('/delete/<bot_number:int>', method='POST')
def delete_bot(bot_number):
    return json.dumps(proc.delete_bot_db(bot_number))


@route('/delete_all')
def delete_all_bots():
    return json.dumps(proc.delete_all_bots_db())

