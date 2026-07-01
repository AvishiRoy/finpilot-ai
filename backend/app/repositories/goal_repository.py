from sqlalchemy.orm import Session
from app.models.goal import Goal


class GoalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(self, user_id: int, status: str | None = None) -> list[Goal]:
        query = self.db.query(Goal).filter(Goal.user_id == user_id)
        if status:
            query = query.filter(Goal.status == status)
        return query.order_by(Goal.created_at.desc()).all()

    def get_by_id_for_user(self, goal_id: int, user_id: int) -> Goal | None:
        return (
            self.db.query(Goal)
            .filter(Goal.id == goal_id, Goal.user_id == user_id)
            .first()
        )

    def create(self, data: dict, user_id: int) -> Goal:
        goal = Goal(**data, user_id=user_id)
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def update(self, goal: Goal, updates: dict) -> Goal:
        for field, value in updates.items():
            setattr(goal, field, value)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def delete(self, goal: Goal) -> None:
        self.db.delete(goal)
        self.db.commit()