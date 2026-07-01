from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository

router = APIRouter(prefix="/transactions", tags=["transactions"])

from fastapi import Path

@router.get("/summary/{year}/{month}", response_model=dict)
def monthly_summary(
    year: int = Path(ge=2000, le=2100),
    month: int = Path(ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
        """
        Returns income, expenses, net savings, and savings rate
        for a given month. The AI assistant will use this to answer
        monthly financial health questions.
        """
        return _service(db).get_monthly_summary(current_user.id, year, month)


def _service(db: Session) -> TransactionService:
    return TransactionService(TransactionRepository(db), CategoryRepository(db))


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return _service(db).create_transaction(payload, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=dict)
def list_transactions(
    type: str | None = Query(default=None),
    category_id: int | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = _service(db).list_transactions(
        current_user.id, type, category_id, start_date, end_date, limit, offset
    )
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [TransactionResponse.model_validate(t) for t in items],
    }


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return _service(db).get_transaction(transaction_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return _service(db).update_transaction(transaction_id, payload, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        _service(db).delete_transaction(transaction_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))