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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS palworld_bans (
            id TEXT PRIMARY KEY
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

def insert_palworld_bans(ban_ids):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.executemany("INSERT OR IGNORE INTO palworld_bans (id) VALUES (?)", [(ban_id,) for ban_id in ban_ids])
    conn.commit()
    conn.close()
    
def get_palworld_bans():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM palworld_bans")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

create_db()
