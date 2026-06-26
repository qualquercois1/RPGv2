import sqlite3

def get_connection():
    return sqlite3.connect('rpg.db', check_same_thread=False)

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_characters_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            eye_color TEXT,
            skin_color TEXT,
            classe TEXT,
            height REAL,
            physical TEXT,
            race TEXT,
            region TEXT,
            attribute_strength INTEGER,
            attribute_agility INTEGER,
            attribute_vitality INTEGER,
            attribute_intelligence INTEGER,
            attribute_survival INTEGER,
            attribute_magic INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def create_tables():
    create_users_table()
    create_characters_table()