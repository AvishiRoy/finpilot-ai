from sqlalchemy import (
    Column, Integer, String, Numeric,
    Date, ForeignKey, DateTime, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )

    title = Column(String, nullable=False)        # e.g. "Netflix", "Rent", "EMI"
    type = Column(String, nullable=False)          # "income" | "expense"
    amount = Column(Numeric(12, 2), nullable=False)

    # frequency: "daily" | "weekly" | "monthly" | "yearly"
    frequency = Column(String(20), nullable=False, default="monthly")

    # The day of month this recurs (for monthly frequency).
    day_of_month = Column(Integer, nullable=True)  # 1–31

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)         # NULL = no end date

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    category = relationship("Category")