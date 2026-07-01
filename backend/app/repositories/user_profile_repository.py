from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile


class UserProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> UserProfile | None:
        return (
            self.db.query(UserProfile)
            .filter(UserProfile.user_id == user_id)
            .first()
        )

    def create(self, user_id: int, data: dict) -> UserProfile:
        profile = UserProfile(user_id=user_id, **data)
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update(self, profile: UserProfile, updates: dict) -> UserProfile:
        for field, value in updates.items():
            setattr(profile, field, value)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update_onboarding_step(
        self, profile: UserProfile, step: int, complete: bool = False
    ) -> UserProfile:
        profile.onboarding_step = step
        profile.onboarding_complete = complete
        self.db.commit()
        self.db.refresh(profile)
        return profile