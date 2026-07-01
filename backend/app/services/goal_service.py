from datetime import date
from decimal import Decimal
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal import GoalCreate, GoalUpdate
from app.models.goal import Goal


class GoalService:
    def __init__(self, repo: GoalRepository):
        self.repo = repo

    def create_goal(self, data: GoalCreate, user_id: int) -> Goal:
        return self.repo.create(data.model_dump(), user_id)

    def list_goals(self, user_id: int, status: str | None) -> list[dict]:
        """
        Returns goals enriched with progress data.
        The AI assistant uses this enriched format directly.
        """
        goals = self.repo.get_all_for_user(user_id, status)
        return [self._enrich(g) for g in goals]

    def get_goal(self, goal_id: int, user_id: int) -> dict:
        goal = self.repo.get_by_id_for_user(goal_id, user_id)
        if goal is None:
            raise ValueError("Goal not found.")
        return self._enrich(goal)

    def update_goal(self, goal_id: int, data: GoalUpdate, user_id: int) -> dict:
        goal = self.repo.get_by_id_for_user(goal_id, user_id)
        if goal is None:
            raise ValueError("Goal not found.")
        updates = data.model_dump(exclude_none=True)

        # Auto-mark complete if current_amount reaches target_amount.
        if "current_amount" in updates:
            target = updates.get("target_amount", float(goal.target_amount))
            if float(updates["current_amount"]) >= float(target):
                updates["is_completed"] = True
                updates["status"] = "completed"

        updated = self.repo.update(goal, updates)
        return self._enrich(updated)

    def delete_goal(self, goal_id: int, user_id: int) -> None:
        goal = self.repo.get_by_id_for_user(goal_id, user_id)
        if goal is None:
            raise ValueError("Goal not found.")
        self.repo.delete(goal)

    def _enrich(self, goal: Goal) -> dict:
        """
        Adds calculated fields to a goal.
        This is the structured data the AI will use to give advice like:
        'You need to save ₹12,500/month to reach your house goal on time.'
        """
        target = float(goal.target_amount)
        current = float(goal.current_amount)
        remaining = max(target - current, 0)
        progress_pct = round((current / target * 100), 2) if target > 0 else 0.0

        months_remaining = None
        monthly_required = None
        if goal.target_date:
            today = date.today()
            months_remaining = max(
                (goal.target_date.year - today.year) * 12
                + (goal.target_date.month - today.month),
                0,
            )
            monthly_required = (
                round(remaining / months_remaining, 2)
                if months_remaining > 0
                else remaining
            )

        return {
            "id": goal.id,
            "user_id": goal.user_id,
            "title": goal.title,
            "description": goal.description,
            "target_amount": target,
            "current_amount": current,
            "remaining_amount": remaining,
            "progress_pct": progress_pct,
            "target_date": goal.target_date,
            "months_remaining": months_remaining,
            "monthly_savings_required": monthly_required,
            "status": goal.status,
            "category": goal.category,
            "is_completed": goal.is_completed,
        }