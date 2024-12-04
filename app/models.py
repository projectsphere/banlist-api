from pydantic import BaseModel

class BanUser(BaseModel):
    name: str
    id: str
    reason: str
