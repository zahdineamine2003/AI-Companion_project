import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cyber_friend.db')

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS moods (
            date TEXT PRIMARY KEY,
            mood TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS journal (
            date TEXT PRIMARY KEY,
            text TEXT -- TODO: encrypt
        )''')
        self.conn.commit()

    def save_mood(self, date, mood):
        c = self.conn.cursor()
        c.execute('REPLACE INTO moods (date, mood) VALUES (?, ?)', (date, mood))
        self.conn.commit()

    def get_moods(self, limit=7):
        c = self.conn.cursor()
        c.execute('SELECT date, mood FROM moods ORDER BY date DESC LIMIT ?', (limit,))
        return c.fetchall()

    def save_journal(self, date, text):
        c = self.conn.cursor()
        c.execute('REPLACE INTO journal (date, text) VALUES (?, ?)', (date, text))
        self.conn.commit()

    def get_journal(self, date):
        c = self.conn.cursor()
        c.execute('SELECT text FROM journal WHERE date=?', (date,))
        row = c.fetchone()
        return row[0] if row else None 