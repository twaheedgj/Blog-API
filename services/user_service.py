from models import user
from schemas import USER 
from typing import Optional
from sqlalchemy.orm import Session
class user_service:
    def create_user(self, user: user, db: Session) -> Optional[USER]:
        """
        create a user if not exists
        """
        existing_user = db.query(USER).filter(
            (USER.username == user.username) | (USER.email == user.email)
        ).first()
        if existing_user:
            return None
        user_data = USER(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name if user.last_name is not None else "",
            username=user.username,
            hashed_password=user.password  # In a real application, hash the password
        )
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data

    def get_user(self, username: str, db: Session) -> Optional[USER]:
        return db.query(USER).filter(USER.username == username).first()

    def update_user(self, username: str, user: user, db: Session) -> Optional[user]:
        existing_user = db.query(USER).filter(USER.username == username).first()
        if existing_user:
            for key, value in user.dict().items():
                setattr(existing_user, key, value)
            db.commit()
            db.refresh(existing_user)
            return existing_user
        return None

    def delete_user(self, user_id: int,db:Session) -> None:
        # Logic to delete a user
        pass