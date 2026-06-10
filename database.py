import sqlite3

DB_PATH = "dormitory.db"

def get_dormitory_info(key: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM dormitory_info WHERE key = ?", (key,))
    row = cursor.fetchone()

    conn.close()
    return row[0] if row else "Информация не найдена"

def get_all_dormitory_data() -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT key, value FROM dormitory_info")
    rows = cursor.fetchall()

    conn.close()
    return {key: value for key, value in rows}
