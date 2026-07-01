from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)

    # month and year define the period this budget applies to.
    # A budget is always for one specific month.
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    # A user can only have one budget per category per month.
    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "month", "year",
                         name="uq_budget_user_category_month"),
    )

    user = relationship("User")
    category = relationship("Category")