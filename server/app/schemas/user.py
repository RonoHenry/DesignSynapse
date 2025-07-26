from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional, List
from datetime import datetime
from .base import TimestampMixin

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=150)
    email: EmailStr

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class UserCreate(UserBase):
    password: constr(min_length=8)

    @validator('password')
    def password_strength(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=150)] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase, TimestampMixin):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(UserInDB):
    pass

class UserWithProjects(UserResponse):
    projects: List['ProjectResponse'] = []
