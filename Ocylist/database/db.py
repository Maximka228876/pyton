import sqlite3

def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            reg_date TEXT
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            text TEXT,
            time TEXT,
            active BOOLEAN
        )''')
    conn.commit()
    conn.close()