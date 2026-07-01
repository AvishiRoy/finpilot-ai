from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    @staticmethod
    def create(db: Session, user: UserCreate):
        return UserRepository.create(db, user)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise ValueError(f"User with id {user_id} does not exist.")

        return user