from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm          # new import
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import TokenResponse                      # LoginRequest no longer used in route
from app.schemas.user import UserResponse
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    # OAuth2PasswordRequestForm reads application/x-www-form-urlencoded.
    # This is what Swagger's Authorize button sends — fixing the 422 error.
    # form_data.username holds the email (OAuth2 calls it 'username' by spec).
    # form_data.password holds the plaintext password.
    # Nothing else about the auth flow changes.
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate a user and return a JWT access token.

    Accepts application/x-www-form-urlencoded with fields:
      - username: the user's email address
      - password: the user's plaintext password

    Returns a Bearer token on success.
    Returns 401 for any credential failure (email not found OR wrong password)
    using an identical message to prevent user enumeration.
    """
    repo = UserRepository(db)

    # form_data.username is the email — OAuth2 spec names this field 'username'
    # but we treat it as an email address throughout the application.
    user = repo.get_by_email(form_data.username)

    # Unified error: wrong email and wrong password return the same response.
    # This prevents an attacker from learning which emails are registered.
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """
    Return the profile of the currently authenticated user.
    Unchanged from Task 6.
    """
    return current_user