from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from app.models.enum import UserRole

class UserCreate(BaseModel):
    name: str = Field(
        min_length=3, 
        max_length=100
        # TODO: Regex
    )
    email: EmailStr
    password: str = Field(
        min_length=8, 
        max_length=100
        # TODO:  Regex
    )

class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    email: EmailStr | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    