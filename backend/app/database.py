import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "events.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                code TEXT,
                description TEXT
            )
        """)
        conn.commit()

def save_event(timestamp, code, description):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO events (timestamp, code, description) VALUES (?, ?, ?)",
                  (timestamp, code, description))
        conn.commit()

def get_events():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT timestamp, code, description FROM events ORDER BY id DESC")
        return [{"timestamp": r[0], "code": r[1], "description": r[2]} for r in c.fetchall()]
