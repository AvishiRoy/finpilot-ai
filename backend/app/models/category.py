from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # type distinguishes income categories from expense categories.
    # Allowed values: "income" | "expense"
    # Stored as a plain string now; an Enum column can be added later
    # via migration once the value set is proven stable.
    type = Column(String, nullable=False)

    # is_default = True means this category is visible to ALL users
    # and was seeded by the system (e.g. "Food", "Salary").
    # is_default = False means it was created by a specific user.
    is_default = Column(Boolean, default=False, nullable=False)

    # NULL user_id means this is a system/default category.
    # A non-NULL user_id means this category belongs to that user only.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    # Relationships — not loaded eagerly, used when explicitly joined.
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")