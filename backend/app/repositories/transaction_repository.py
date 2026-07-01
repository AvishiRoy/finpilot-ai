from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_for_user(self, transaction_id: int, user_id: int) -> Transaction | None:
        """Fetch only if this transaction belongs to this user."""
        return (
            self.db.query(Transaction)
            .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
            .first()
        )

    def get_all_for_user(
        self,
        user_id: int,
        type: str | None = None,
        category_id: int | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Transaction], int]:
        """
        Returns a page of transactions plus the total count.
        All filters are user-scoped — impossible to retrieve another user's data.
        Returns (items, total) so the API can return pagination metadata.
        """
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)

        if type:
            query = query.filter(Transaction.type == type)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        total = query.count()
        items = query.order_by(Transaction.date.desc()).offset(offset).limit(limit).all()
        return items, total

    def create(self, data: dict, user_id: int) -> Transaction:
        transaction = Transaction(**data, user_id=user_id)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def update(self, transaction: Transaction, updates: dict) -> Transaction:
        for field, value in updates.items():
            setattr(transaction, field, value)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete(self, transaction: Transaction) -> None:
        self.db.delete(transaction)
        self.db.commit()

    def get_monthly_totals(self, user_id: int, year: int, month: int) -> dict:
        """
        Returns total income and total expenses for a given month.
        Used by the monthly summary and dashboard endpoints.
        """
        from sqlalchemy import func, extract
        result = (
            self.db.query(
                Transaction.type,
                func.sum(Transaction.amount).label("total")
            )
            .filter(
                Transaction.user_id == user_id,
                extract("year", Transaction.date) == year,
                extract("month", Transaction.date) == month,
            )
            .group_by(Transaction.type)
            .all()
        )
        totals = {"income": 0, "expense": 0}
        for row in result:
            totals[row.type] = float(row.total)
        return totals
    
    def get_spending_by_category(
        self, user_id: int, start_date: date, end_date: date
    ) -> list[dict]:
        """
        Returns expense totals grouped by category for a date range.
        Used by analytics and future AI spending pattern analysis.
        """
        from sqlalchemy import func
        from app.models.category import Category

        results = (
            self.db.query(
                Category.name.label("category"),
                func.sum(Transaction.amount).label("total"),
                func.count(Transaction.id).label("count"),
            )
            .join(Category, Transaction.category_id == Category.id, isouter=True)
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == "expense",
                Transaction.date >= start_date,
                Transaction.date <= end_date,
            )
            .group_by(Category.name)
            .order_by(func.sum(Transaction.amount).desc())
            .all()
        )
        return [
            {
                "category": row.category or "Uncategorized",
                "total": float(row.total),
                "count": row.count,
            }
            for row in results
        ]