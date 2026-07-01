from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import date
from typing import Optional

VALID_FREQUENCIES = {"daily", "weekly", "monthly", "yearly"}


class RecurringTransactionCreate(BaseModel):
    title: str
    type: str
    amount: Decimal
    frequency: str = "monthly"
    day_of_month: Optional[int] = None
    start_date: date
    end_date: Optional[date] = None
    category_id: Optional[int] = None

    @field_validator("type")
    @classmethod
    def valid_type(cls, v: str) -> str:
        if v not in ("income", "expense"):
            raise ValueError("type must be 'income' or 'expense'.")
        return v

    @field_validator("frequency")
    @classmethod
    def valid_frequency(cls, v: str) -> str:
        if v not in VALID_FREQUENCIES:
            raise ValueError(f"frequency must be one of {VALID_FREQUENCIES}")
        return v

    @field_validator("amount")
    @classmethod
    def positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("amount must be greater than zero.")
        return v


class RecurringTransactionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    type: str
    amount: Decimal
    frequency: str
    day_of_month: Optional[int]
    start_date: date
    end_date: Optional[date]
    is_active: bool
    category_id: Optional[int]

    model_config = {"from_attributes": True}