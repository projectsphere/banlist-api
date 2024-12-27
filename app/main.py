from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
import app.database as db
from app.models import BanUser
import app.settings as settings
import aiohttp

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
BEARER_TOKEN = settings.bearer_token

@app.on_event("startup")
async def startup_event():
    await db.create_db()

@app.post("/api/banuser")
async def ban_user(ban_user: BanUser, token: str = Depends(oauth2_scheme)):
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    await db.add_ban(ban_user.name, ban_user.id, ban_user.reason)
    return {"message": "User banned successfully"}

@app.post("/api/unbanuser")
async def unban_user(steamid: str, token: str = Depends(oauth2_scheme)):
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    success = await db.remove_ban(steamid)
    if not success:
        raise HTTPException(status_code=404, detail="User not found in banlist")

    return {"message": f"User with ID {steamid} has been unbanned successfully"}

@app.get("/api/banlist.txt", response_class=PlainTextResponse)
async def get_public_banlist():
    my_bans = await db.get_ban()
    palworld_bans = await db.get_palworld_bans()
    all_bans = [ban["id"] for ban in my_bans] + palworld_bans
    formatted_content = "\n".join(all_bans)
    return PlainTextResponse(formatted_content, media_type="text/plain")

@app.get("/api/bannedusers")
async def banned_users(token: str = Depends(oauth2_scheme), name: str = Query(None)):
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    if name:
        return await db.get_ban_name(name)
    return await db.get_ban()

@app.post("/api/syncbans")
async def sync_palworld_bans(token: str = Depends(oauth2_scheme)):
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    url = "https://api.palworldgame.com/api/banlist.txt"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=500, detail=f"Failed to fetch banlist: {response.status}")
                data = await response.text()
                ban_ids = data.strip().split()
                await db.insert_palworld_bans(ban_ids)
                return {"message": f"{len(ban_ids)} bans synced successfully"}
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Palworld bans: {str(e)}")
