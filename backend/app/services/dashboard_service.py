from datetime import date
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.budget_repository import BudgetRepository


class DashboardService:
    def __init__(self, tx_repo: TransactionRepository, budget_repo: BudgetRepository):
        self.tx_repo = tx_repo
        self.budget_repo = budget_repo

    def get_dashboard(self, user_id: int) -> dict:
        today = date.today()
        year, month = today.year, today.month

        # Monthly income / expense totals
        totals = self.tx_repo.get_monthly_totals(user_id, year, month)
        income = totals["income"]
        expense = totals["expense"]
        net = round(income - expense, 2)
        savings_rate = round((net / income * 100), 2) if income > 0 else 0.0

        # Spending by category this month
        start = date(year, month, 1)
        spending_by_category = self.tx_repo.get_spending_by_category(
            user_id, start, today
        )

        # Budget utilization — compare actual spending against set budgets
        budgets = self.budget_repo.get_all_for_user(user_id, month, year)
        budget_status = []
        for b in budgets:
            spent = next(
                (s["total"] for s in spending_by_category
                 if s["category"] == (b.category.name if b.category else None)),
                0.0,
            )
            limit = float(b.amount)
            budget_status.append({
                "category_id": b.category_id,
                "category": b.category.name if b.category else "Unknown",
                "budget": limit,
                "spent": spent,
                "remaining": round(limit - spent, 2),
                "utilization_pct": round(spent / limit * 100, 2) if limit > 0 else 0.0,
                "is_over_budget": spent > limit,
            })

        return {
            "period": {"year": year, "month": month},
            "summary": {
                "total_income": income,
                "total_expenses": expense,
                "net_savings": net,
                "savings_rate_pct": savings_rate,
            },
            "top_spending_categories": spending_by_category[:5],
            "budget_status": budget_status,
            "alerts": [
                f"Over budget on {b['category']} by ₹{abs(b['remaining']):.2f}"
                for b in budget_status if b["is_over_budget"]
            ],
        }