import sqlite3

conn = sqlite3.connect("aes.db")
cursor = conn.cursor()

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
cursor.execute("ALTER TABLE videos ADD COLUMN view_count INTEGER;")
cursor.execute("ALTER TABLE videos ADD COLUMN duration TEXT;")
cursor.execute("ALTER TABLE videos ADD COLUMN channel_logo TEXT;")




                
conn.close()
