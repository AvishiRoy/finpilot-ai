from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        return UserRepository.create(db, user)