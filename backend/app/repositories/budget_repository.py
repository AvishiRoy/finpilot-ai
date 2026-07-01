from sqlalchemy.orm import Session
from app.models.budget import Budget


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(self, user_id: int, month: int, year: int) -> list[Budget]:
        return (
            self.db.query(Budget)
            .filter(Budget.user_id == user_id, Budget.month == month, Budget.year == year)
            .all()
        )

    def get_by_id_for_user(self, budget_id: int, user_id: int) -> Budget | None:
        return (
            self.db.query(Budget)
            .filter(Budget.id == budget_id, Budget.user_id == user_id)
            .first()
        )

    def get_existing(self, user_id: int, category_id: int, month: int, year: int) -> Budget | None:
        return (
            self.db.query(Budget)
            .filter(
                Budget.user_id == user_id,
                Budget.category_id == category_id,
                Budget.month == month,
                Budget.year == year,
            )
            .first()
        )

    def create(self, data: dict, user_id: int) -> Budget:
        budget = Budget(**data, user_id=user_id)
        self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)
        return budget

    def delete(self, budget: Budget) -> None:
        self.db.delete(budget)
        self.db.commit()