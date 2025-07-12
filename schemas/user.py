from sqlmodel import Field, SQLModel, Relationship
import uuid
from sqlalchemy.dialects.postgresql import *


class USER(SQLModel, table=True):
    """User model for the application."""
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=100, unique=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    is_active: bool = Field(default=False)
    username: str = Field(max_length=10, unique=True)
    hashed_password: str = Field(max_length=100)