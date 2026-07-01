from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """
    Create a signed JWT access token.

    'subject' is the value that identifies who this token belongs to —
    we use the user's email (a stable, unique identifier).

    The token payload contains:
    - 'sub': the subject (user email) — standard JWT claim name
    - 'exp': expiry timestamp — jose validates this automatically on decode

    The token is signed with SECRET_KEY using the HS256 algorithm.
    Anyone with the secret key can verify the token's authenticity,
    but without it the signature cannot be forged — this is what makes
    the token trustworthy without a database lookup on every request.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": subject,
        "exp": expire,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> str | None:
    """
    Decode and verify a JWT access token.
    Returns the subject (user email) if valid, None if invalid or expired.
    Used in Task 5 and later when protecting routes.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload.get("sub")
    except JWTError:
        return None