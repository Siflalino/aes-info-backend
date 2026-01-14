import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "aes.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id TEXT UNIQUE,
        title TEXT,
        description TEXT,
        channel TEXT,
        channel_logo TEXT,
        views INTEGER,
        duration TEXT,
        published_at TEXT,
        country TEXT,
        platform TEXT
    )
    """)

    conn.commit()
    conn.close()


