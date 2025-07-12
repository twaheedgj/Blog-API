from fastapi import APIRouter, Depends, HTTPException
from services import userservice
from models import user
from db import get_session
user_router = APIRouter()


@user_router.post("/create_account")
async def signup(user: user, db=Depends(get_session)):
    """
    Create a new user account.
    """
    if not user.email or not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Email, username, and password are required.")
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")
    return userservice.create_user(user, db)