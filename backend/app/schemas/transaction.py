from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date
from decimal import Decimal


class TransactionCreate(BaseModel):
    type: str                          # "income" or "expense"
    amount: Decimal
    description: Optional[str] = None
    date: date
    category_id: Optional[int] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("income", "expense"):
            raise ValueError("type must be 'income' or 'expense'.")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("amount must be greater than zero.")
        return v


class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    date: Optional[date] = None
    category_id: Optional[int] = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v <= 0:
            raise ValueError("amount must be greater than zero.")
        return v


class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: Decimal
    description: Optional[str]
    date: date
    user_id: int
    category_id: Optional[int]

    model_config = {"from_attributes": True}