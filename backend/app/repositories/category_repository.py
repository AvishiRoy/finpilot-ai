from sqlalchemy.orm import Session
from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(self, user_id: int) -> list[Category]:
        """
        Returns system-default categories (user_id IS NULL)
        plus this user's own custom categories.
        Never returns another user's categories.
        """
        return (
            self.db.query(Category)
            .filter(
                (Category.is_default == True) |
                (Category.user_id == user_id)
            )
            .order_by(Category.type, Category.name)
            .all()
        )

    def get_by_id(self, category_id: int) -> Category | None:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_id_for_user(self, category_id: int, user_id: int) -> Category | None:
        """
        Fetches a category only if it is a default OR belongs to this user.
        Used before creating a transaction to validate the category reference.
        """
        return (
            self.db.query(Category)
            .filter(
                Category.id == category_id,
                (Category.is_default == True) | (Category.user_id == user_id)
            )
            .first()
        )

    def create(self, name: str, type: str, user_id: int, description: str | None) -> Category:
        category = Category(
            name=name,
            type=type,
            user_id=user_id,
            description=description,
            is_default=False,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()

    def seed_defaults(self) -> None:
        """
        Insert system-wide default categories if they do not already exist.
        Called once at application startup from main.py.
        """
        defaults = [
            {"name": "Salary",        "type": "income"},
            {"name": "Freelance",     "type": "income"},
            {"name": "Business",      "type": "income"},
            {"name": "Investment",    "type": "income"},
            {"name": "Other Income",  "type": "income"},
            {"name": "Food",          "type": "expense"},
            {"name": "Transport",     "type": "expense"},
            {"name": "Housing",       "type": "expense"},
            {"name": "Healthcare",    "type": "expense"},
            {"name": "Education",     "type": "expense"},
            {"name": "Shopping",      "type": "expense"},
            {"name": "Entertainment", "type": "expense"},
            {"name": "Utilities",     "type": "expense"},
            {"name": "Savings",       "type": "expense"},
            {"name": "Other Expense", "type": "expense"},
        ]
        for item in defaults:
            exists = (
                self.db.query(Category)
                .filter(Category.name == item["name"], Category.is_default == True)
                .first()
            )
            if not exists:
                self.db.add(Category(
                    name=item["name"],
                    type=item["type"],
                    is_default=True,
                    user_id=None,
                ))
        self.db.commit()