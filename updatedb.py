import sqlite3

DB_PATH = "C:/Users/flamb/Desktop/app_mobile/aes_info_app/backend/data/aes.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

columns = {
    "views": "INTEGER",
    "duration": "TEXT",
    "channel_logo": "TEXT"
}

for column, col_type in columns.items():
    try:
        cursor.execute(f"ALTER TABLE videos ADD COLUMN {column} {col_type}")
        print(f"✅ Colonne ajoutée : {column}")
    except sqlite3.OperationalError:
        print(f"ℹ️ Colonne déjà existante : {column}")

conn.commit()
conn.close()

print("🎯 Base de données mise à jour avec succès")
