import aiosqlite
import os

DB_FILE = os.path.join('data', 'bans.db')

async def create_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                userid TEXT NOT NULL UNIQUE,
                reason TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS palworld_bans (
                id TEXT PRIMARY KEY
            )
        """)
        await db.commit()

async def add_ban(name: str, userid: str, reason: str):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("INSERT INTO bans (name, userid, reason) VALUES (?, ?, ?)", (name, userid, reason))
        await db.commit()
    
async def remove_ban(userid: str) -> bool:
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("DELETE FROM bans WHERE userid = ?", (userid,))
        changes = cursor.rowcount
        await db.commit()
        return changes > 0

async def get_ban():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT name, userid, reason FROM bans")
        rows = await cursor.fetchall()
        return [{"name": row[0], "id": row[1], "reason": row[2]} for row in rows]

async def get_ban_name(name: str):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT name, userid, reason FROM bans WHERE name LIKE ?", (f"%{name}%",))
        rows = await cursor.fetchall()
        return [{"name": row[0], "id": row[1], "reason": row[2]} for row in rows]

async def insert_palworld_bans(ban_ids):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.executemany("INSERT OR IGNORE INTO palworld_bans (id) VALUES (?)", [(ban_id,) for ban_id in ban_ids])
        await db.commit()
    
async def get_palworld_bans():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT id FROM palworld_bans")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]
