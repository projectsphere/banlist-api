from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
import app.db_utils as db
from app.models import BanUser
import app.settings as settings

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
BEARER_TOKEN = settings.bearer_token

@app.post("/api/banuser")
async def ban_user(ban_user: BanUser, token: str = Depends(oauth2_scheme)):
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    db.add_ban(ban_user.name, ban_user.id, ban_user.reason)
    return {"message": "User banned successfully"}

@app.get("/api/banlist.txt", response_class=PlainTextResponse)
async def get_public_banlist():
    bans = db.get_ban()
    formatted_content = " ".join([ban["id"] for ban in bans])
    return PlainTextResponse(formatted_content, media_type="text/plain")

@app.get("/api/bannedusers")
async def banned_users(token: str = Depends(oauth2_scheme)):
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return db.get_ban()
