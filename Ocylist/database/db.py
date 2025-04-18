import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def init_db():
    # Подключение к PostgreSQL
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            reg_date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            text TEXT,
            time TEXT,
            active BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()