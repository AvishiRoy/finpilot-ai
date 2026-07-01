from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import hash_password
from app.api import user  

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    
    def get_user_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise ValueError(f"User with id {user_id} does not exist.")

        return user
    
    def create_user(self, data: UserCreate) -> User:
        """
        Hash the incoming password, then delegate to the repository.
        The repository receives a hashed_password string — it never
        sees or stores the original plaintext password.
        """
        existing = self.repository.get_by_email(data.email)
        if existing:
            raise ValueError(f"Email {data.email} is already registered.")
        
        """print(data.password)
        print(len(data.password))

        print("PASSWORD =", data.password)
        print("LENGTH =", len(data.password))"""

        hashed = hash_password(data.password)
        return self.repository.create(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hashed,
    )

    def update_user(self, user_id: int, updates: UserUpdate) -> User:
        """
        Fetch user (raises ValueError if missing), validate email,
        then perform a partial update.
        """
        user = self.get_user_by_id(user_id)

        update_data = updates.model_dump(exclude_none=True)

        if not update_data:
            return user

        # Check email uniqueness only if email is being changed
        if "email" in update_data:
            existing = self.repository.get_by_email(update_data["email"])

            if existing and existing.id != user.id:
                raise ValueError("Email already exists.")

        return self.repository.update(user, update_data)

    def delete_user(self, user_id: int) -> None:
        """
        Fetch user (raises ValueError if missing), then delegate
        deletion to the repository. Returns nothing.
        """
        user = self.get_user_by_id(user_id)
        self.repository.delete(user)

