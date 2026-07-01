from sqlalchemy import (
    Column, Integer, String, Numeric,
    Date, ForeignKey, DateTime, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # The total amount the user wants to reach.
    target_amount = Column(Numeric(12, 2), nullable=False)

    # How much the user has saved toward this goal so far.
    # Updated manually or automatically from tagged transactions later.
    current_amount = Column(Numeric(12, 2), default=0, nullable=False)

    # Deadline — used by the AI to calculate required monthly savings.
    target_date = Column(Date, nullable=True)

    # status: "active" | "completed" | "cancelled"
    status = Column(String(20), default="active", nullable=False, index=True)

    # Category of goal — used for AI categorization and advice.
    # e.g. "emergency_fund" | "house" | "car" | "education" | "travel" | "other"
    category = Column(String(50), default="other", nullable=False)

    is_completed = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User", back_populates="goals")