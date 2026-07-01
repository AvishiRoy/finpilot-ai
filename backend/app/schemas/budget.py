from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Optional


class BudgetCreate(BaseModel):
    category_id: int
    amount: Decimal
    month: int
    year: int

    @field_validator("amount")
    @classmethod
    def positive_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Budget amount must be greater than zero.")
        return v

    @field_validator("month")
    @classmethod
    def valid_month(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("month must be between 1 and 12.")
        return v


class BudgetResponse(BaseModel):
    id: int
    category_id: int
    amount: Decimal
    month: int
    year: int
    user_id: int

    model_config = {"from_attributes": True}