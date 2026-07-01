from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    #@staticmethod
    def create(self, user: UserCreate):
        db_user = User(
            full_name=user.full_name,
            email=user.email,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    #@staticmethod
    def get_by_id(self, user_id: int) -> User | None:
        """
        Fetch a user by primary key.
        Returns None if no user exists.
        """
        return self.db.query(User).filter(User.id == user_id).first()