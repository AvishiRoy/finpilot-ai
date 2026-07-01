from sqlalchemy import (
    Column, Integer, String, Numeric,
    ForeignKey, DateTime, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    # One profile per user — enforced by unique constraint on user_id.
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # Personal financial identity
    monthly_income = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(10), default="INR", nullable=False)
    employment_status = Column(String(50), nullable=True)
    # e.g. "salaried" | "self_employed" | "student" | "unemployed" | "retired"

    # Risk tolerance drives future investment recommendations
    risk_tolerance = Column(String(20), nullable=True)
    # e.g. "conservative" | "moderate" | "aggressive"

    # Onboarding progress — tracked as a step number so the frontend
    # knows exactly where to resume if the user closes the app mid-flow.
    onboarding_step = Column(Integer, default=0, nullable=False)
    onboarding_complete = Column(Boolean, default=False, nullable=False)

    # AI personalization fields
    financial_goal_summary = Column(String, nullable=True)
    # A short text the user writes: "I want to buy a house in 3 years"
    # Stored here so the AI always has a top-level intent available.

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship back to User
    user = relationship("User", back_populates="profile")