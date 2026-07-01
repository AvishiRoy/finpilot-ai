from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    type: str           # "income" or "expense"
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str]
    is_default: bool
    user_id: Optional[int]

    model_config = {"from_attributes": True}