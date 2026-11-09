from database import get_connection, init_db

init_db()

conn = get_connection()
conn.execute(
    "INSERT INTO notes (title, content) VALUES (?, ?)",
    ("Catatan pertama", "Ini isi catatan dari database"),
)
conn.commit()
conn.close()

print("Data percobaan berhasil ditambahkan")

