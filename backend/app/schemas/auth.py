from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """
    Credentials submitted by the user at login.
    Email and password — nothing else.
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Response returned after successful login.

    access_token: the signed JWT the client stores and sends on
                  subsequent requests via Authorization: Bearer header.
    token_type:   always "bearer" — this is the OAuth2 convention that
                  tells clients how to use the token.
    """
    access_token: str
    token_type: str = "bearer"