from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.recurring_transaction import RecurringTransaction
from app.schemas.recurring_transaction import (
    RecurringTransactionCreate,
    RecurringTransactionResponse,
)

router = APIRouter(prefix="/recurring", tags=["recurring"])


@router.post("/", response_model=RecurringTransactionResponse, status_code=201)
def create_recurring(
    payload: RecurringTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = RecurringTransaction(**payload.model_dump(), user_id=current_user.id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[RecurringTransactionResponse])
def list_recurring(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.user_id == current_user.id,
            RecurringTransaction.is_active == True,
        )
        .all()
    )


@router.delete("/{record_id}", status_code=204)
def deactivate_recurring(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.id == record_id,
            RecurringTransaction.user_id == current_user.id,
        )
        .first()
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Recurring transaction not found.")
    record.is_active = False    # soft delete — keep history
    db.commit()