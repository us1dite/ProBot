import sqlite3

db = sqlite3.connect('db')
cursor = db.cursor()

lucky = """CREATE TABLE IF NOT EXISTS studens
    (
        id INTEGER PRIMARY KEY, 
        role TEXT
    ),

        CREATE TABLE IF NOT EXISTS teachers
    (
        id INTEGER PRIMARY KEY,
        role TEXT
    )
"""
cursor.executescript(lucky)
