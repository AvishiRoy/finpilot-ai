from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Optional

VALID_EMPLOYMENT = {
    "salaried", "self_employed", "student", "unemployed", "retired"
}
VALID_RISK = {"conservative", "moderate", "aggressive"}


class UserProfileCreate(BaseModel):
    monthly_income: Optional[Decimal] = None
    currency: str = "INR"
    employment_status: Optional[str] = None
    risk_tolerance: Optional[str] = None
    financial_goal_summary: Optional[str] = None

    @field_validator("employment_status")
    @classmethod
    def validate_employment(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_EMPLOYMENT:
            raise ValueError(f"employment_status must be one of {VALID_EMPLOYMENT}")
        return v

    @field_validator("risk_tolerance")
    @classmethod
    def validate_risk(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_RISK:
            raise ValueError(f"risk_tolerance must be one of {VALID_RISK}")
        return v

    @field_validator("monthly_income")
    @classmethod
    def validate_income(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v < 0:
            raise ValueError("monthly_income cannot be negative.")
        return v


class UserProfileUpdate(BaseModel):
    monthly_income: Optional[Decimal] = None
    currency: Optional[str] = None
    employment_status: Optional[str] = None
    risk_tolerance: Optional[str] = None
    financial_goal_summary: Optional[str] = None

    @field_validator("employment_status")
    @classmethod
    def validate_employment(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_EMPLOYMENT:
            raise ValueError(f"employment_status must be one of {VALID_EMPLOYMENT}")
        return v

    @field_validator("risk_tolerance")
    @classmethod
    def validate_risk(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_RISK:
            raise ValueError(f"risk_tolerance must be one of {VALID_RISK}")
        return v


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    monthly_income: Optional[Decimal]
    currency: str
    employment_status: Optional[str]
    risk_tolerance: Optional[str]
    financial_goal_summary: Optional[str]
    onboarding_step: int
    onboarding_complete: bool

    model_config = {"from_attributes": True}