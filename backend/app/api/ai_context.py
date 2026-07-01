from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.ai_context_service import AIContextService
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.budget_repository import BudgetRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_profile_repository import UserProfileRepository

router = APIRouter(prefix="/ai", tags=["ai-context"])


@router.get("/context", response_model=dict)
def get_ai_context(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the complete structured financial context for the current user.

    This endpoint is the bridge between the financial data layer and the
    AI layer. When the chat module is built, it will call this first,
    then inject the result into the LLM system prompt so the AI has
    full awareness of the user's financial situation before responding.
    """
    service = AIContextService(
        user=current_user,
        tx_repo=TransactionRepository(db),
        budget_repo=BudgetRepository(db),
        goal_repo=GoalRepository(db),
        profile_repo=UserProfileRepository(db),
    )
    return service.build()