from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Authenticate a user and return a JWT access token.

    Security note: both "user not found" and "wrong password" return the
    same 401 response with the same message. This is deliberate — returning
    different messages for each case would allow an attacker to enumerate
    valid email addresses by observing which error they receive
    (a technique called user enumeration). Identical error responses
    prevent this information leak.
    """
    repo = UserRepository(db)
    user = repo.get_by_email(payload.email)

    # Unified check: wrong email and wrong password look identical to caller.
    if user is None or not verify_password(payload.password, user.hashed_password):
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