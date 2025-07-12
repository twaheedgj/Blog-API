from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class Image(SQLModel, table=True):
    __tablename__ = "blog_images"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str
    public_id: str
    blog_id: uuid.UUID = Field(foreign_key="blog_posts.id")
    
    # Relationship back to BlogPost
    blog: Optional["BlogPost"] = Relationship(back_populates="images")


class BlogPost(SQLModel, table=True):
    __tablename__ = "blog_posts"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # One-to-many relationship to images
    images: List[Image] = Relationship(back_populates="blog")
