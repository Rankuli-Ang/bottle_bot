from bottle import route
import configparser
import json
from src.processor import Processor
import sqlite3
import time

db = 'resources/bots.db'
proc = Processor(db)  # It's not good to create proc here, but I can't come up better decision


@route('/')
def get_tutorial():
    """Displays all commands."""
    data = {"commands": [
        {'bot/bot_number': 'returns bot statistics(method=POST)'},
        {'bots': 'returns statistics for all bots(method=GET)'},
        {'/move/bot_number/target_x/target_y': 'moves bot with a given values(method=POST)'},
        {'create/x/y': 'creates bot with a given values(method=POST)'},
        {'delete/bot_number': 'deletes bot with a given number(method=POST)'},
        {'delete_all': 'deletes all bots (only if everyone is stopped)(method=GET)'}]}
    return json.dumps(data)


@route('/bot/<bot_number:int>', method="POST")
def get_bot(bot_number) -> str:
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
def get_bots() -> str:
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
def move(bot_number, target_x, target_y) -> str:
    """Moves bot with a given values."""
    conn = sqlite3.connect(r'resources/bots.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bots WHERE id = ? ORDER BY id DESC LIMIT 1  """, (bot_number,))
    bot_stats = cur.fetchone()
    if bot_stats is None:
        return json.dumps({'bot': 'is not exist'})
    proc.add_bot_to_proc(bot_stats)
    current_bot = proc.get_current_bot_instance(bot_stats[0])
    if current_bot.is_moving:
        return json.dumps({'bot': proc.current_bot_is_moving(current_bot)})
    proc.bot_move(current_bot, target_x, target_y)
    return json.dumps({"movement": "is over"})


@route('/create/<x:int>/<y:int>', method='POST')
def create_bot(x, y) -> str:
    """Creates new bot with a given coordinates."""
    return json.dumps(proc.create_bot(x, y))


@route('/delete/<bot_number:int>', method='POST')
def delete_bot(bot_number) -> str:
    """Deletes bot with a given number."""
    return json.dumps(proc.delete_bot(bot_number))


@route('/delete_all')
def delete_all_bots() -> str:
    """Deletes all bots."""
    return json.dumps(proc.delete_all_bots())

