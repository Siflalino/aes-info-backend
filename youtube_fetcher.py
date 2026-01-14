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

API_KEY = os.environ.get("YOUTUBE_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ YOUTUBE_API_KEY manquante")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "aes.db")

youtube = build("youtube", "v3", developerKey=API_KEY)


def parse_duration(duration):
    duration = duration.replace("PT", "")
    minutes = seconds = 0

    if "M" in duration:
        minutes = int(duration.split("M")[0])
        duration = duration.split("M")[1]

    if "S" in duration:
        seconds = int(duration.replace("S", ""))

    return f"{minutes}:{str(seconds).zfill(2)}"


def video_exists(cursor, video_id):
    cursor.execute(
        "SELECT 1 FROM videos WHERE video_id = ? LIMIT 1",
        (video_id,)
    )
    return cursor.fetchone() is not None


def fetch_videos(query, country, max_results=10):
    try:
        response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results,
            order="date"
        ).execute()
    except Exception as e:
        print(f"❌ Recherche YouTube échouée : {e}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    added = 0

    for item in response.get("items", []):
        try:
            video_id = item["id"]["videoId"]

            # 🔥 NE PAS IGNORER SILENCIEUSEMENT
            if video_exists(cursor, video_id):
                continue

            snippet = item["snippet"]

            video_data = youtube.videos().list(
                part="statistics,contentDetails",
                id=video_id
            ).execute()["items"][0]

            views = int(video_data["statistics"].get("viewCount", 0))
            duration = parse_duration(video_data["contentDetails"]["duration"])

            channel_data = youtube.channels().list(
                part="snippet",
                id=snippet["channelId"]
            ).execute()["items"][0]

            channel_logo = channel_data["snippet"]["thumbnails"]["default"]["url"]

            cursor.execute("""
                INSERT INTO videos (
                    video_id, title, description, channel,
                    channel_logo, views, duration,
                    published_at, country, platform
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

            added += 1

        except Exception as e:
            print(f"⚠️ Vidéo ignorée : {e}")

    conn.commit()
    conn.close()

    print(f"✅ {added} nouvelles vidéos ajoutées pour {country}")


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
        fetch_videos(query, country)
        time.sleep(1)

    print("🚀 Mise à jour YouTube terminée")




