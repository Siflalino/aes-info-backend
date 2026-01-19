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


# from flask import Flask, jsonify
# from flask_cors import CORS
# import sqlite3
# import os

# from youtube_fetcher import fetch_all
# from database import init_db   # 🔥 IMPORTANT

# app = Flask(__name__)
# CORS(app)

# # 📦 Base de données (Render + local)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "data", "aes.db")


# def get_db():
#     return sqlite3.connect(DB_PATH, check_same_thread=False)


# # 🔥 INITIALISATION AU DÉMARRAGE
# init_db()

# try:
#     fetch_all()
#     print("✅ Vidéos chargées au démarrage")
# except Exception as e:
#     print("⚠️ Erreur fetch initial :", e)


# # 🩺 HEALTH CHECK (Render)
# @app.route("/")
# def health():
#     return jsonify({"status": "ok"})


# # 🔄 REFRESH MANUEL (test navigateur / postman)
# @app.route("/refresh", methods=["GET", "POST"])
# def refresh_videos():
#     try:
#         fetch_all()
#         return jsonify({
#             "status": "success",
#             "message": "✅ Vidéos mises à jour"
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500


# # 📺 API PRINCIPALE POUR FLUTTER
# @app.route("/videos")
# def get_videos():
#     conn = get_db()
#     cursor = conn.cursor()

#     # 🔥 Vérifier si la DB est vide
#     cursor.execute("SELECT COUNT(*) FROM videos")
#     count = cursor.fetchone()[0]

#     if count == 0:
#         try:
#             fetch_all()
#         except Exception as e:
#             print("⚠️ Fetch auto échoué :", e)

#     cursor.execute("""
#         SELECT id, video_id, title, description, channel,
#                channel_logo, views, duration,
#                published_at, country, platform
#         FROM videos
#         ORDER BY datetime(published_at) DESC
#         LIMIT 100
#     """)

#     rows = cursor.fetchall()
#     conn.close()

#     return jsonify([
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
#     ])


from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os
import threading

from youtube_fetcher import fetch_all
from database import init_db

app = Flask(__name__)
CORS(app)

# 📦 Base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "aes.db")


def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# 🔥 INIT DB (safe)
init_db()


# 🔥 FETCH AU DÉMARRAGE (UNE SEULE FOIS)
def background_fetch():
    try:
        print("🚀 Chargement initial des vidéos...")
        fetch_all()
        print("✅ Vidéos chargées")
    except Exception as e:
        print("⚠️ Erreur fetch initial :", e)


# 🚀 Lancer le fetch en arrière-plan (non bloquant)
threading.Thread(target=background_fetch, daemon=True).start()



# 🩺 HEALTH CHECK AVEC STATUT DB
@app.route("/")
@app.route("/health")
def health():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM videos")
    count = cursor.fetchone()[0]
    conn.close()

    return jsonify({
        "status": "ok",
        "videos": count
    })


# 🔄 REFRESH MANUEL
@app.route("/refresh", methods=["GET", "POST"])
def refresh_videos():
    try:
        threading.Thread(target=fetch_all).start()
        return jsonify({
            "status": "success",
            "message": "🔄 Mise à jour lancée"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 📺 API PRINCIPALE
@app.route("/videos")
def get_videos():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, video_id, title, description, channel,
               channel_logo, views, duration,
               published_at, country, platform
        FROM videos
        ORDER BY datetime(published_at) DESC
        LIMIT 100
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([
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
    ])






