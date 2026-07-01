from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("/", response_model=BudgetResponse, status_code=201)
def create_budget(
    payload: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = BudgetRepository(db)
    # Prevent duplicate budget for same category/month/year
    existing = repo.get_existing(
        current_user.id, payload.category_id, payload.month, payload.year
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A budget for this category and month already exists."
        )
    return repo.create(payload.model_dump(), current_user.id)


@router.get("/", response_model=list[BudgetResponse])
def list_budgets(
    month: int = Query(ge=1, le=12),
    year: int = Query(ge=2000, le=2100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BudgetRepository(db).get_all_for_user(current_user.id, month, year)


@router.delete("/{budget_id}", status_code=204)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = BudgetRepository(db)
    budget = repo.get_by_id_for_user(budget_id, current_user.id)
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found.")
    repo.delete(budget)