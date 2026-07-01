from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # type: "income" or "expense" — denormalized from category for fast filtering.
    # Storing it here means you can filter by type without joining categories.
    type = Column(String, nullable=False, index=True)

    # Numeric(12, 2) stores up to 999,999,999,999.99 — avoids float precision
    # issues that would corrupt financial calculations.
    amount = Column(Numeric(12, 2), nullable=False)

    description = Column(String, nullable=True)

    # The date the transaction actually occurred (not when it was entered).
    # Stored as Date (not DateTime) because financial reports are always
    # date-based, not time-based.
    date = Column(Date, nullable=False, index=True)

    # Composite index on (user_id, date) because the most common query pattern
    # is "all transactions for user X between date A and date B".
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"),
                         nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")