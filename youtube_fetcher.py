# from googleapiclient.discovery import build
# import sqlite3
# import time

# API_KEY = "AIzaSyDIIf6FTyXT0pno7ErMrT0ZtUc2862ZBp4"
# DB_PATH = "C:/Users/flamb/Desktop/app_mobile/aes_info_app/backend/data/aes.db"

# youtube = build("youtube", "v3", developerKey=API_KEY)

# def fetch_videos(query, country, max_results=20):
#     search_request = youtube.search().list(
#         q=query,
#         part="snippet",
#         type="video",
#         maxResults=max_results,
#         order="date"
#     )
#     search_response = search_request.execute()

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     for item in search_response["items"]:
#         video_id = item["id"]["videoId"]
#         snippet = item["snippet"]

#         # 📊 stats + durée
#         video_request = youtube.videos().list(
#             part="statistics,contentDetails",
#             id=video_id
#         )
#         video_response = video_request.execute()
#         stats = video_response["items"][0]

#         views = stats["statistics"].get("viewCount", 0)
#         duration = stats["contentDetails"]["duration"]

#         # 🖼 logo chaîne
#         channel_request = youtube.channels().list(
#             part="snippet",
#             id=snippet["channelId"]
#         )
#         channel_response = channel_request.execute()
#         channel_logo = channel_response["items"][0]["snippet"]["thumbnails"]["default"]["url"]

#         cursor.execute("""
#         INSERT OR IGNORE INTO videos
#         (video_id, title, description, channel, channel_logo,
#          views, duration, published_at, country, platform)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             video_id,
#             snippet["title"],
#             snippet["description"],
#             snippet["channelTitle"],
#             channel_logo,
#             views,
#             duration,
#             snippet["publishedAt"],
#             country,
#             "YouTube"
#         ))

#     conn.commit()
#     conn.close()


# if __name__ == "__main__":
#     queries = [
#         ("Burkina Faso", "RTB Burkina Faso actualité"),
#         ("Burkina Faso", "Burkina Faso journal télévisé"),
#         ("Mali", "ORTM Mali actualité"),
#         ("Mali", "Mali journal télévisé"),
#         ("Niger", "Télé Sahel Niger actualité"),
#         ("Niger", "Niger journal télévisé"),
#         ("AES", "Alliance des États du Sahel actualité"),
#     ]

#     for country, query in queries:
#         fetch_videos(query, country, max_results=15)
#         time.sleep(1)  # éviter le quota

#     print("✅ Vidéos multi-pays sauvegardées")


# from googleapiclient.discovery import build
# import sqlite3
# import time

# API_KEY = "AIzaSyDIIf6FTyXT0pno7ErMrT0ZtUc2862ZBp4"
# DB_PATH = "C:/Users/flamb/Desktop/app_mobile/aes_info_app/backend/data/aes.db"

# youtube = build("youtube", "v3", developerKey=API_KEY)

# def fetch_videos(query, country, max_results=20):
#     search_request = youtube.search().list(
#         q=query,
#         part="snippet",
#         type="video",
#         maxResults=max_results,
#         order="date"
#     )
#     search_response = search_request.execute()

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     for item in search_response["items"]:
#         video_id = item["id"]["videoId"]
#         snippet = item["snippet"]

#         video_request = youtube.videos().list(
#             part="statistics,contentDetails",
#             id=video_id
#         )
#         video_response = video_request.execute()
#         stats = video_response["items"][0]

#         views = stats["statistics"].get("viewCount", 0)
#         duration = stats["contentDetails"]["duration"]

#         channel_request = youtube.channels().list(
#             part="snippet",
#             id=snippet["channelId"]
#         )
#         channel_response = channel_request.execute()
#         channel_logo = channel_response["items"][0]["snippet"]["thumbnails"]["default"]["url"]

#         cursor.execute("""
#         INSERT OR IGNORE INTO videos
#         (video_id, title, description, channel, channel_logo,
#          views, duration, published_at, country, platform)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             video_id,
#             snippet["title"],
#             snippet["description"],
#             snippet["channelTitle"],
#             channel_logo,
#             views,
#             duration,
#             snippet["publishedAt"],
#             country,
#             "YouTube"
#         ))

#     conn.commit()
#     conn.close()


# # ✅ NOUVELLE FONCTION
# def fetch_all():
#     queries = [
#         ("Burkina Faso", "RTB Burkina Faso actualité"),
#         ("Burkina Faso", "Burkina Faso journal télévisé"),
#         ("Mali", "ORTM Mali actualité"),
#         ("Mali", "Mali journal télévisé"),
#         ("Niger", "Télé Sahel Niger actualité"),
#         ("Niger", "Niger journal télévisé"),
#         ("AES", "Alliance des États du Sahel actualité"),
#     ]

#     for country, query in queries:
#         fetch_videos(query, country, max_results=15)
#         time.sleep(1)  # éviter quota

#     print("✅ Vidéos mises à jour")


from googleapiclient.discovery import build
import sqlite3
import time
import os
import re

# 🔐 API KEY (Render)
API_KEY = os.environ.get("YOUTUBE_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ YOUTUBE_API_KEY manquante")

# 📦 Base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "aes.db")

youtube = build("youtube", "v3", developerKey=API_KEY)

# ⏱️ Convertir durée ISO 8601 → secondes
def parse_duration(duration):
    if not duration:
        return 0

    h = re.search(r'(\d+)H', duration)
    m = re.search(r'(\d+)M', duration)
    s = re.search(r'(\d+)S', duration)

    return (
        int(h.group(1)) * 3600 if h else 0
    ) + (
        int(m.group(1)) * 60 if m else 0
    ) + (
        int(s.group(1)) if s else 0
    )

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# 🔍 Recherche générique
def fetch_videos(query, country, max_results=15):
    print(f"🔍 {country} | {query}")

    try:
        response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results,
            order="date"
        ).execute()
    except Exception as e:
        print(f"❌ Erreur YouTube search : {e}")
        return

    conn = get_connection()
    cursor = conn.cursor()
    added = 0

    for item in response.get("items", []):
        try:
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]

            video_resp = youtube.videos().list(
                part="statistics,contentDetails",
                id=video_id
            ).execute()

            if not video_resp["items"]:
                continue

            video_data = video_resp["items"][0]

            views = int(video_data["statistics"].get("viewCount", 0))
            duration = parse_duration(video_data["contentDetails"]["duration"])

            channel_resp = youtube.channels().list(
                part="snippet",
                id=snippet["channelId"]
            ).execute()

            channel_logo = channel_resp["items"][0]["snippet"]["thumbnails"]["default"]["url"]

            cursor.execute("""
                INSERT OR IGNORE INTO videos (
                    video_id, title, description, channel,
                    channel_logo, views, duration,
                    published_at, country, platform
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                video_id,
                snippet["title"],
                snippet["description"],
                snippet["channelTitle"],
                channel_logo,
                views,
                duration,
                snippet["publishedAt"],
                country,
                "YouTube"
            ))

            if cursor.rowcount > 0:
                added += 1

        except Exception as e:
            print(f"⚠️ Vidéo ignorée ({video_id}) : {e}")

    conn.commit()
    conn.close()

    print(f"✅ {added} nouvelles vidéos ajoutées ({country})")

# 🚀 MISE À JOUR GLOBALE
def fetch_all():
    print("🔄 Mise à jour YouTube globale")

    SEARCH_CONFIG = {
        "Burkina Faso": [
            "RTB Burkina Faso",
            "Burkina Faso actualité",
            "Burkina Faso journal télévisé",
            "IB Traoré discours",
            "AES Burkina Faso",
            "politique Burkina Faso",
        ],
        "Mali": [
            "ORTM Mali",
            "actualité Mali",
            "journal télévisé Mali",
            "Assimi Goïta discours",
            "AES Mali",
        ],
        "Niger": [
            "Télé Sahel Niger",
            "actualité Niger",
            "journal télévisé Niger",
            "Abdourahamane Tiani",
            "AES Niger",
        ],
        "AES": [
            "Alliance des États du Sahel",
            "Confédération AES",
            "sommet AES",
            "actualité AES",
            "AES Mali Burkina Niger",
        ]
    }

    for country, queries in SEARCH_CONFIG.items():
        for query in queries:
            fetch_videos(query, country)
            time.sleep(1.2)  # anti quota YouTube

    print("🚀 Mise à jour YouTube terminée")






