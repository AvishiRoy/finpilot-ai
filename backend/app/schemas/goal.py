from pydantic import BaseModel, field_validator
from decimal import Decimal
from datetime import date
from typing import Optional

VALID_STATUSES = {"active", "completed", "cancelled"}
VALID_CATEGORIES = {
    "emergency_fund", "house", "car", "education",
    "travel", "investment", "retirement", "other"
}


class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_amount: Decimal
    current_amount: Decimal = Decimal("0")
    target_date: Optional[date] = None
    category: str = "other"

    @field_validator("target_amount", "current_amount")
    @classmethod
    def non_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Amount cannot be negative.")
        return v

    @field_validator("category")
    @classmethod
    def valid_category(cls, v: str) -> str:
        if v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {VALID_CATEGORIES}")
        return v


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[Decimal] = None
    current_amount: Optional[Decimal] = None
    target_date: Optional[date] = None
    status: Optional[str] = None
    category: Optional[str] = None

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        return v


class GoalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    target_amount: Decimal
    current_amount: Decimal
    target_date: Optional[date]
    status: str
    category: str
    is_completed: bool

    model_config = {"from_attributes": True}