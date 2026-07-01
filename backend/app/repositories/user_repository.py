import email

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    #@staticmethod
    def create(self, email: str, full_name: str | None, hashed_password: str) -> User:
        """
        Persist a new user with a pre-hashed password.
        The repository never hashes anything itself — it receives
        already-processed values from the service layer.
        """
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    #@staticmethod
    def get_by_id(self, user_id: int) -> User | None:
        """
        Fetch a user by primary key.
        Returns None if no user exists.
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()