from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalUpdate
from app.services.goal_service import GoalService
from app.repositories.goal_repository import GoalRepository

router = APIRouter(prefix="/goals", tags=["goals"])


def _service(db: Session) -> GoalService:
    return GoalService(GoalRepository(db))


@router.post("/", response_model=dict, status_code=201)
def create_goal(
    payload: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service(db).create_goal(payload, current_user.id)


@router.get("/", response_model=list)
def list_goals(
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _service(db).list_goals(current_user.id, status)


@router.get("/{goal_id}", response_model=dict)
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return _service(db).get_goal(goal_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{goal_id}", response_model=dict)
def update_goal(
    goal_id: int,
    payload: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return _service(db).update_goal(goal_id, payload, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{goal_id}", status_code=204)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        _service(db).delete_goal(goal_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))