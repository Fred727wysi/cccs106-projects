# src/test_db.py
from db_connection import connect_db

try:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users;")
    rows = cursor.fetchall()
    conn.close()
    print("✅ DB connected. Found rows:")
    for r in rows:
        print(r)
except Exception as e:
    print("❌ DB connection FAILED:", e)
