from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr


class UserResponse(UserCreate):
    id: int

    model_config = {
        "from_attributes": True
    }