from pydantic import BaseModel, EmailStr
from typing import Optional



class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):      # <-- NOT UserCreate
    id: int
    full_name: Optional[str] = None
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
