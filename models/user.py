from pydantic import BaseModel
from typing import Optional
class user(BaseModel):
    email: str
    first_name: str 
    last_name: Optional[str]
    username: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

class UserInDB(user):
    hashed_password: str