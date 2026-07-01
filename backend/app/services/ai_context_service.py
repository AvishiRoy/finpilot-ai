from datetime import date
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.budget_repository import BudgetRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_profile_repository import UserProfileRepository
from app.models.user import User


class AIContextService:
    """
    Assembles a complete, structured financial context object for a user.
    This is the payload that will be injected into the LLM system prompt
    so the AI has full financial awareness before answering any question.

    Keeping this as its own service means:
    - It can be called from the chat endpoint without duplicating logic.
    - It can be cached (Redis) later when performance matters.
    - It can be unit-tested independently of the LLM layer.
    """

    def __init__(
        self,
        user: User,
        tx_repo: TransactionRepository,
        budget_repo: BudgetRepository,
        goal_repo: GoalRepository,
        profile_repo: UserProfileRepository,
    ):
        self.user = user
        self.tx_repo = tx_repo
        self.budget_repo = budget_repo
        self.goal_repo = goal_repo
        self.profile_repo = profile_repo

    def build(self) -> dict:
        today = date.today()
        year, month = today.year, today.month
        user_id = self.user.id

        profile = self.profile_repo.get_by_user_id(user_id)
        monthly_totals = self.tx_repo.get_monthly_totals(user_id, year, month)
        income = monthly_totals["income"]
        expense = monthly_totals["expense"]

        start_of_month = date(year, month, 1)
        spending_by_category = self.tx_repo.get_spending_by_category(
            user_id, start_of_month, today
        )

        budgets = self.budget_repo.get_all_for_user(user_id, month, year)
        budget_summary = [
            {
                "category": b.category.name if b.category else "Unknown",
                "budget": float(b.amount),
                "spent": next(
                    (s["total"] for s in spending_by_category
                     if s["category"] == (b.category.name if b.category else None)),
                    0.0,
                ),
            }
            for b in budgets
        ]

        goals = self.goal_repo.get_all_for_user(user_id, status="active")
        goal_summary = [
            {
                "title": g.title,
                "target": float(g.target_amount),
                "saved": float(g.current_amount),
                "target_date": str(g.target_date) if g.target_date else None,
                "category": g.category,
            }
            for g in goals
        ]

        # Recent transactions give the AI short-term spending awareness.
        recent_tx, _ = self.tx_repo.get_all_for_user(
            user_id, limit=10, offset=0
        )

        return {
            "user": {
                "name": self.user.full_name,
                "email": self.user.email,
            },
            "profile": {
                "monthly_income": float(profile.monthly_income) if profile and profile.monthly_income else None,
                "currency": profile.currency if profile else "INR",
                "employment_status": profile.employment_status if profile else None,
                "risk_tolerance": profile.risk_tolerance if profile else None,
                "financial_goal_summary": profile.financial_goal_summary if profile else None,
            },
            "current_month": {
                "year": year,
                "month": month,
                "total_income": income,
                "total_expenses": expense,
                "net_savings": round(income - expense, 2),
                "savings_rate_pct": round((income - expense) / income * 100, 2) if income > 0 else 0.0,
            },
            "spending_by_category": spending_by_category,
            "budgets": budget_summary,
            "active_goals": goal_summary,
            "recent_transactions": [
                {
                    "type": t.type,
                    "amount": float(t.amount),
                    "description": t.description,
                    "date": str(t.date),
                }
                for t in recent_tx
            ],
        }