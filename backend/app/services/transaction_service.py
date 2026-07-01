from datetime import date
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.models.transaction import Transaction


class TransactionService:
    def __init__(self, repo: TransactionRepository, category_repo: CategoryRepository):
        self.repo = repo
        self.category_repo = category_repo

    def create_transaction(self, data: TransactionCreate, user_id: int) -> Transaction:
        """
        Validate the category belongs to this user (or is a default),
        then create the transaction.
        """
        if data.category_id is not None:
            category = self.category_repo.get_by_id_for_user(data.category_id, user_id)
            if category is None:
                raise ValueError("Category not found or does not belong to you.")
            # Enforce consistency: transaction type must match category type.
            if category.type != data.type:
                raise ValueError(
                    f"Category is of type '{category.type}' "
                    f"but transaction type is '{data.type}'."
                )

        payload = data.model_dump()
        return self.repo.create(payload, user_id)

    def get_transaction(self, transaction_id: int, user_id: int) -> Transaction:
        """Raises ValueError if not found or belongs to another user."""
        transaction = self.repo.get_by_id_for_user(transaction_id, user_id)
        if transaction is None:
            raise ValueError("Transaction not found.")
        return transaction

    def list_transactions(
        self,
        user_id: int,
        type: str | None,
        category_id: int | None,
        start_date: date | None,
        end_date: date | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Transaction], int]:
        return self.repo.get_all_for_user(
            user_id, type, category_id, start_date, end_date, limit, offset
        )

    def update_transaction(
        self, transaction_id: int, data: TransactionUpdate, user_id: int
    ) -> Transaction:
        transaction = self.get_transaction(transaction_id, user_id)
        updates = data.model_dump(exclude_none=True)
        if not updates:
            return transaction
        return self.repo.update(transaction, updates)

    def delete_transaction(self, transaction_id: int, user_id: int) -> None:
        transaction = self.get_transaction(transaction_id, user_id)
        self.repo.delete(transaction)

    def get_monthly_summary(self, user_id: int, year: int, month: int) -> dict:
        totals = self.repo.get_monthly_totals(user_id, year, month)
        income = totals["income"]
        expense = totals["expense"]
        return {
            "year": year,
            "month": month,
            "total_income": income,
            "total_expenses": expense,
            "net_savings": round(income - expense, 2),
            "savings_rate": round((income - expense) / income * 100, 2) if income > 0 else 0.0,
        }