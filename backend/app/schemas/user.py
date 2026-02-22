"""
User schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date
from typing import Optional
from .enums import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    manager_id: Optional[int] = None
    department: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    full_name: Optional[str] = None
    department: Optional[str] = None
    manager_id: Optional[int] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    hire_date: date
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
