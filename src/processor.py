from .bot import Bot
import sqlite3

database = "src/resources/movements.db"

conn = sqlite3.connect(database)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS movements(id INT PRIMARY KEY,x INT, y INT)""")
cur.execute("""SELECT * FROM movements ORDER BY id DESC LIMIT 1""")
coordinates = cur.fetchone()
