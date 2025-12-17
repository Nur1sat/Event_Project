from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    group: Optional[str] = None


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    secret_key: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    group: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    group: Optional[str]
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
