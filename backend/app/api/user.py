from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> UserResponse:
    """
    Create a new user.
    """
    service = UserService(UserRepository(db))
    return service.create_user(user)


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    """List all users. Public for now — RBAC added later."""
    service = UserService(UserRepository(db))
    return service.get_all_users()



@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> UserResponse:
    """
    Fetch a single user by their id.
    Returns 404 if no user with that id exists.
    """
    service = UserService(UserRepository(db))
    try:
        return service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),   # protected
) -> UserResponse:
    """Update a user. Requires authentication."""
    service = UserService(UserRepository(db))
    try:
        return service.update_user(user_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),   # protected
) -> Response:
    """Delete a user. Requires authentication."""
    service = UserService(UserRepository(db))
    try:
        service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=204)
