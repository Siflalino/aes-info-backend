from flask import Flask, jsonify
from flask_cors import CORS
from scheduler import start_scheduler
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = "data/aes.db"

@app.route("/videos")
def get_videos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, video_id, title, description, channel,
           channel_logo, views, duration,
           published_at, country, platform
    FROM videos
    ORDER BY published_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    videos = [
        {
            "id": r[0],
            "video_id": r[1],
            "title": r[2],
            "description": r[3],
            "channel": r[4],
            "channel_logo": r[5],
            "views": r[6],
            "duration": r[7],
            "published_at": r[8],
            "country": r[9],
            "platform": r[10],
        }
        for r in rows
    ]

    return jsonify(videos)


if __name__ == "__main__":
    start_scheduler()  # 🔥 TÂCHE AUTO
    app.run(debug=True)
