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
from dotenv import load_dotenv

load_dotenv()

# 🔐 API KEY (Render + Local)
API_KEY = os.getenv("AIzaSyDIIf6FTyXT0pno7ErMrT0ZtUc2862ZBp4")

# 📦 Base de données (Render compatible)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "aes.db")

youtube = build("youtube", "v3", developerKey=API_KEY)


# 🔁 Convertir durée ISO 8601 → lisible
def parse_duration(duration):
    duration = duration.replace("PT", "")
    minutes = seconds = 0

    if "M" in duration:
        minutes = int(duration.split("M")[0])
        duration = duration.split("M")[1]

    if "S" in duration:
        seconds = int(duration.replace("S", ""))

    return f"{minutes}:{str(seconds).zfill(2)}"


def fetch_videos(query, country, max_results=15):
    try:
        search_request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results,
            order="date"
        )
        search_response = search_request.execute()
    except Exception as e:
        print(f"❌ Erreur recherche YouTube : {e}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for item in search_response.get("items", []):
        try:
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]

            # 🎥 Infos vidéo
            video_request = youtube.videos().list(
                part="statistics,contentDetails",
                id=video_id
            )
            video_response = video_request.execute()

            if not video_response["items"]:
                continue

            stats = video_response["items"][0]
            views = int(stats["statistics"].get("viewCount", 0))
            duration = parse_duration(stats["contentDetails"]["duration"])

            # 📺 Logo chaîne
            channel_request = youtube.channels().list(
                part="snippet",
                id=snippet["channelId"]
            )
            channel_response = channel_request.execute()
            channel_logo = channel_response["items"][0]["snippet"]["thumbnails"]["default"]["url"]

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

        except Exception as e:
            print(f"⚠️ Vidéo ignorée : {e}")
            continue

    conn.commit()
    conn.close()


# 🔥 FONCTION PRINCIPALE
def fetch_all():
    queries = [
        ("Burkina Faso", "RTB Burkina Faso actualité"),
        ("Burkina Faso", "Burkina Faso journal télévisé"),
        ("Mali", "ORTM Mali actualité"),
        ("Mali", "Mali journal télévisé"),
        ("Niger", "Télé Sahel Niger actualité"),
        ("Niger", "Niger journal télévisé"),
        ("AES", "Alliance des États du Sahel actualité"),
    ]

    for country, query in queries:
        fetch_videos(query, country, max_results=10)
        time.sleep(1)  # éviter quota

    print("✅ Vidéos YouTube mises à jour")


