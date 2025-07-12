from typing import List, Optional
from .images import ImageCreate, ImageRead
from pydantic import BaseModel
from datetime import datetime
import uuid
class BlogPostCreate(BaseModel):
    title: str
    description: str
    content: str
    images: List[ImageCreate] = []

class BlogPostRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    content: str
    images: List[ImageRead]
    created_at: datetime    

    class Config:
        orm_mode = True
        
        
class BlogPostUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    content: Optional[str]
    
    class Config:
        orm_mode = True