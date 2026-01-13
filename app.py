# from flask import Flask, jsonify
# from flask_cors import CORS
# from scheduler import start_scheduler
# import sqlite3

# app = Flask(__name__)
# CORS(app)

# DB_PATH = "data/aes.db"

# @app.route("/videos")
# def get_videos():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute("""
#     SELECT id, video_id, title, description, channel,
#            channel_logo, views, duration,
#            published_at, country, platform
#     FROM videos
#     ORDER BY published_at DESC
#     """)

#     rows = cursor.fetchall()
#     conn.close()

#     videos = [
#         {
#             "id": r[0],
#             "video_id": r[1],
#             "title": r[2],
#             "description": r[3],
#             "channel": r[4],
#             "channel_logo": r[5],
#             "views": r[6],
#             "duration": r[7],
#             "published_at": r[8],
#             "country": r[9],
#             "platform": r[10],
#         }
#         for r in rows
#     ]

#     return jsonify(videos)


# if __name__ == "__main__":
#     start_scheduler()  # 🔥 TÂCHE AUTO
#     app.run(debug=True)


# from flask import Flask, jsonify

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return jsonify({"status": "Backend OK"})

# @app.route("/health")
# def health():
#     return {"status": "ok"}

# if __name__ == "__main__":
#     app.run()


# from flask import Flask, jsonify
# from flask_cors import CORS
# import sqlite3
# import os

# from youtube_fetcher import fetch_all
# from scheduler import start_scheduler

# app = Flask(__name__)
# CORS(app)

# # 📦 Chemin DB compatible Render + local
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "data", "aes.db")


# def get_db_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


# @app.route("/videos", methods=["GET"])
# def get_videos():
#     # 🔥 Mise à jour AVANT d'envoyer les données
#     fetch_all()

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT id, video_id, title, description, channel,
#                channel_logo, views, duration,
#                published_at, country, platform
#         FROM videos
#         ORDER BY published_at DESC
#         LIMIT 100
#     """)

#     rows = cursor.fetchall()
#     conn.close()

#     videos = [dict(row) for row in rows]
#     return jsonify(videos)


# # 🔥 IMPORTANT POUR RENDER
# if __name__ == "__main__":
#     start_scheduler()  # Une seule fois en local
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
from scheduler import start_scheduler

app = Flask(__name__)
CORS(app)

DB_PATH = "data/aes.db"

# 🔥 DÉMARRER LE SCHEDULER AU DÉMARRAGE DU SERVEUR
start_scheduler()

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

    videos = [{
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
    } for r in rows]

    return jsonify(videos)

