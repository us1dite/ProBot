import sqlite3

def create_connection():
    return sqlite3.connect('database.db')

def create_tables():
    conn = create_connection()
    curs = conn.cursor()

    curs.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            username TEXT,
            role TEXT
        )
    """)

    curs.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT 
        )
    """)

    curs.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT 
        )
    """)

    curs.execute("""
        CREATE TABLE IF NOT EXISTS user_groups (
            user_id INTEGER,
            group_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (group_id) REFERENCES groups (id),
            PRIMARY KEY (user_id, group_id)
        )
    """)

    curs.execute("""
        CREATE TABLE IF NOT EXISTS groups_of_teachers (
            teacher_id INTEGER,
            group_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id),
            FOREIGN KEY (group_id) REFERENCES groups (id),
            PRIMARY KEY (teacher_id, group_id)
        )
    """)

    curs.execute("""
        CREATE TABLE IF NOT EXISTS users_and_teachers (
            teacher_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id),
            FOREIGN KEY (user_id) REFERENCES groups (id),
            PRIMARY KEY (teacher_id, user_id)
        )
    """)

    conn.commit()
    conn.close()

