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


from googleapiclient.discovery import build
import sqlite3
import time

API_KEY = "AIzaSyDIIf6FTyXT0pno7ErMrT0ZtUc2862ZBp4"
DB_PATH = "C:/Users/flamb/Desktop/app_mobile/aes_info_app/backend/data/aes.db"

youtube = build("youtube", "v3", developerKey=API_KEY)

def fetch_videos(query, country, max_results=20):
    search_request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results,
        order="date"
    )
    search_response = search_request.execute()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for item in search_response["items"]:
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]

        video_request = youtube.videos().list(
            part="statistics,contentDetails",
            id=video_id
        )
        video_response = video_request.execute()
        stats = video_response["items"][0]

        views = stats["statistics"].get("viewCount", 0)
        duration = stats["contentDetails"]["duration"]

        channel_request = youtube.channels().list(
            part="snippet",
            id=snippet["channelId"]
        )
        channel_response = channel_request.execute()
        channel_logo = channel_response["items"][0]["snippet"]["thumbnails"]["default"]["url"]

        cursor.execute("""
        INSERT OR IGNORE INTO videos
        (video_id, title, description, channel, channel_logo,
         views, duration, published_at, country, platform)
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

    conn.commit()
    conn.close()


# ✅ NOUVELLE FONCTION
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
        fetch_videos(query, country, max_results=15)
        time.sleep(1)  # éviter quota

    print("✅ Vidéos mises à jour")


