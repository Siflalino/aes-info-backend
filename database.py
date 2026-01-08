import sqlite3

DB_PATH = "C:/Users/flamb/Desktop/app_mobile/aes_info_app/backend/data/aes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id TEXT UNIQUE,
        title TEXT,
        description TEXT,
        channel TEXT,
        published_at TEXT,
        country TEXT,
        platform TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Base de données initialisée")
