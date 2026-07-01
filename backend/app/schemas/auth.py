from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """
    JSON-body login schema.

    Not used by the Swagger Authorize flow (which requires form encoding
    per the OAuth2 spec), but retained for:
    - Direct API clients (mobile apps, curl with -H 'Content-Type: application/json')
    - Integration tests that POST JSON
    - Documentation of the expected credential shape

    If you add a separate JSON login endpoint in future, use this schema there.
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Response returned after successful authentication.

    access_token: signed JWT the client sends as 'Authorization: Bearer <token>'
    token_type:   always 'bearer' — the OAuth2 convention for this token format
    """
    access_token: str
    token_type: str = "bearer"