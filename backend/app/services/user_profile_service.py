from app.repositories.user_profile_repository import UserProfileRepository
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate
from app.models.user_profile import UserProfile


class UserProfileService:
    def __init__(self, repo: UserProfileRepository):
        self.repo = repo

    def get_or_create(self, user_id: int) -> UserProfile:
        """
        Returns the user's profile. If no profile exists yet,
        creates a blank one. This means the API never returns 404
        for a profile — every user always has one.
        """
        profile = self.repo.get_by_user_id(user_id)
        if profile is None:
            profile = self.repo.create(user_id, {})
        return profile

    def update_profile(
        self, user_id: int, data: UserProfileUpdate
    ) -> UserProfile:
        profile = self.get_or_create(user_id)
        updates = data.model_dump(exclude_none=True)
        if not updates:
            return profile
        return self.repo.update(profile, updates)