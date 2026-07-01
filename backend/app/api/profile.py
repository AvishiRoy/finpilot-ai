from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user_profile import (
    UserProfileResponse,
    UserProfileUpdate,
)
from app.services.user_profile_service import UserProfileService
from app.repositories.user_profile_repository import UserProfileRepository


from fastapi import HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/profile", tags=["profile"])


def _service(db: Session) -> UserProfileService:
    return UserProfileService(UserProfileRepository(db))


@router.get("/", response_model=UserProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the current user's financial profile.
    Creates a blank profile automatically if one does not exist yet.
    """
    return _service(db).get_or_create(current_user.id)


@router.patch("/", response_model=UserProfileResponse)
def update_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Partially update the current user's financial profile."""
    return _service(db).update_profile(current_user.id, payload)


# Define valid onboarding steps and what each one means.
# Step 0 = not started, Step 5 = complete.
ONBOARDING_STEPS = {
    0: "not_started",
    1: "profile_basic",       # name, employment, currency
    2: "income_entered",      # monthly income set
    3: "goals_set",           # at least one goal created
    4: "first_transaction",   # at least one transaction logged
    5: "complete",
}
MAX_STEP = 5


class OnboardingStepPayload(BaseModel):
    step: int


@router.post("/onboarding/step", response_model=UserProfileResponse)
def advance_onboarding(
    payload: OnboardingStepPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Advance the user's onboarding to the given step.
    Steps must increase sequentially — you cannot skip ahead.
    Marks onboarding complete when step reaches MAX_STEP.
    """
    if payload.step not in ONBOARDING_STEPS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid step. Valid steps are 0–{MAX_STEP}.",
        )

    svc = _service(db)
    profile = svc.get_or_create(current_user.id)

    if payload.step < profile.onboarding_step:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Cannot go back to step {payload.step}. "
                f"Current step is {profile.onboarding_step}."
            ),
        )

    is_complete = payload.step >= MAX_STEP
    repo = UserProfileRepository(db)
    updated = repo.update_onboarding_step(profile, payload.step, is_complete)
    return updated


@router.get("/onboarding/status", response_model=dict)
def onboarding_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the user's current onboarding progress.
    The frontend calls this on app load to decide which screen to show.
    """
    profile = _service(db).get_or_create(current_user.id)
    return {
        "current_step": profile.onboarding_step,
        "step_name": ONBOARDING_STEPS.get(profile.onboarding_step, "unknown"),
        "is_complete": profile.onboarding_complete,
        "total_steps": MAX_STEP,
        "progress_pct": round(profile.onboarding_step / MAX_STEP * 100),
    }