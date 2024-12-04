import sqlite3
import os

DB_FILE = os.path.join('data', 'bans.db')

def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            steamid TEXT NOT NULL UNIQUE,
            reason TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_ban(name: str, steamid: str, reason: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bans (name, steamid, reason) VALUES (?, ?, ?)", (name, steamid, reason))
    conn.commit()
    conn.close()
    
def remove_ban(steamid: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bans WHERE steamid = ?", (steamid,))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes > 0

def get_ban():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, steamid, reason FROM bans")
    rows = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "id": row[1], "reason": row[2]} for row in rows]

create_db()
