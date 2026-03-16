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


# 📝 LETTRE DE MOTIVATION – BOURSE WASCAL MRP-ICC
@app.route("/lettre-motivation/wascal")
def lettre_motivation_wascal():
    lettre = {
        "programme": "Master Research Programme in Informatics for Climate Change (MRP-ICC)",
        "institution": "Université Joseph KI-ZERBO, Ouagadougou, Burkina Faso",
        "session": "2026/2027",
        "organisme": "West African Science Service Centre on Climate Change and Adapted Land Use (WASCAL)",
        "titre": "Lettre de Motivation – Bourse WASCAL MRP-ICC 2026/2027",
        "contenu": (
            "Objet : Candidature au Master Research Programme in Informatics for Climate Change (MRP-ICC) "
            "– Session 2026/2027\n\n"

            "Madame, Monsieur,\n\n"

            "C'est avec un grand intérêt et une profonde conviction que je soumets ma candidature au "
            "Master Research Programme in Informatics for Climate Change (MRP-ICC), organisé par "
            "l'Université Joseph KI-ZERBO de Ouagadougou, Burkina Faso, dans le cadre du programme "
            "de renforcement des capacités du West African Science Service Centre on Climate Change "
            "and Adapted Land Use (WASCAL), avec le soutien du Ministère Fédéral Allemand de la "
            "Recherche, de la Technologie et de l'Espace (BMFTR).\n\n"

            "Titulaire d'un diplôme de licence (BSc) en Informatique avec mention, j'ai acquis de "
            "solides compétences en programmation, en gestion de bases de données, en systèmes "
            "d'information et en analyse de données. Mon parcours académique m'a permis de développer "
            "une maîtrise des outils informatiques avancés ainsi qu'une rigueur méthodologique "
            "indispensable à la conduite de travaux de recherche scientifique.\n\n"

            "La problématique du changement climatique constitue l'un des défis majeurs de notre époque, "
            "en particulier pour les pays d'Afrique de l'Ouest. Face à la récurrence des phénomènes "
            "météorologiques extrêmes, à la dégradation des terres et à la pression croissante sur les "
            "ressources naturelles, il m'est apparu indispensable d'orienter mes compétences "
            "informatiques vers des applications directement utiles à nos populations. C'est ce qui "
            "motive profondément mon souhait d'intégrer ce programme unique, qui associe l'informatique "
            "avancée aux sciences climatiques.\n\n"

            "Le MRP-ICC représente pour moi une opportunité exceptionnelle de me spécialiser dans la "
            "gestion et l'analyse des données climatiques, l'exploitation de systèmes de calcul haute "
            "performance (HPC) et la mise en œuvre de modèles climatiques régionaux. Ces compétences "
            "sont essentielles pour doter l'Afrique de l'Ouest d'une expertise locale capable de "
            "produire des informations climatiques fiables à l'intention des décideurs, des agences "
            "météorologiques nationales et des communautés vulnérables. Je suis particulièrement "
            "attiré par la dimension interdisciplinaire et transdisciplinaire du programme, qui permet "
            "d'aborder les enjeux climatiques dans toute leur complexité.\n\n"

            "Par ailleurs, mon intérêt pour les logiciels d'analyse climatique open source ainsi que "
            "pour l'administration et la maintenance des infrastructures informatiques m'a conduit à "
            "me former de manière autonome sur plusieurs outils pertinents pour ce programme. "
            "Cette curiosité intellectuelle et ma capacité à apprendre en autonomie me permettront "
            "de tirer le meilleur parti des enseignements dispensés à l'Université Joseph KI-ZERBO.\n\n"

            "À l'issue de ce master, mon ambition est de contribuer activement au développement des "
            "services climatiques dans mon pays et dans la sous-région ouest-africaine, que ce soit "
            "au sein des agences météorologiques nationales, des centres de recherche, des universités "
            "ou des institutions internationales travaillant sur l'adaptation au changement climatique. "
            "Je suis également ouvert à la poursuite en doctorat afin d'approfondir mes travaux de "
            "recherche dans ce domaine stratégique.\n\n"

            "Convaincu que WASCAL, avec ses ressources scientifiques et son réseau régional d'excellence, "
            "est le cadre idéal pour développer cette expertise, je m'engage à m'investir pleinement "
            "dans le programme, à respecter l'ensemble des exigences académiques et à mettre en valeur "
            "les connaissances acquises au service du développement durable de l'Afrique de l'Ouest.\n\n"

            "Je reste à votre entière disposition pour tout entretien ou complément d'information "
            "que vous jugerez nécessaire.\n\n"

            "Dans l'espoir que ma candidature retiendra votre attention, je vous prie d'agréer, "
            "Madame, Monsieur, l'expression de ma haute considération.\n\n"

            "[Prénom NOM]\n"
            "[Date]\n"
            "[Adresse – Ville, Pays]\n"
            "[Email] | [Téléphone / WhatsApp]"
        )
    }
    return jsonify(lettre)






