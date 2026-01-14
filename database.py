import sqlite3
import os

# 📦 Chemin portable (Windows + Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "aes.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 🎥 Table vidéos complète
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE,
            title TEXT,
            description TEXT,
            channel TEXT,
            channel_logo TEXT,
            views INTEGER DEFAULT 0,
            duration TEXT,
            published_at TEXT,
            country TEXT,
            platform TEXT
        )
    """)

    # ⚡ Index pour affichage rapide
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_published_at
        ON videos(published_at)
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✅ Base de données initialisée correctement")

