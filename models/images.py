from pydantic import BaseModel
from typing import Optional
import uuid

class ImageRead(BaseModel):
    id: uuid.UUID
    url: str
    public_id: str
    class Config:
        orm_mode = True

class ImageCreate(BaseModel):
    url: str
    public_id: str