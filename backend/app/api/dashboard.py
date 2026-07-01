from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.dashboard_service import DashboardService
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.budget_repository import BudgetRepository

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=dict)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Single endpoint for the frontend dashboard and AI context loading.
    Returns: monthly summary, top spending categories, budget utilization,
    and any over-budget alerts — all scoped to the authenticated user.
    """
    service = DashboardService(TransactionRepository(db), BudgetRepository(db))
    return service.get_dashboard(current_user.id)

@router.get("/net-worth", response_model=dict)
def get_net_worth(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns a lifetime net worth snapshot for the authenticated user.
    Used by the AI to assess overall financial health.
    """
    service = DashboardService(TransactionRepository(db), BudgetRepository(db))
    return service.get_net_worth(current_user.id)