from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    user_name : str = Field(...,min_length=1 ,max_length=50)
    user_email : EmailStr
    user_age : int = Field(...,ge=0 ,le=120)
    user_role: UserRole
    class Config:
        extra = "forbid"

class User(UserBase):
    password: str = Field(min_length=8)
    

class UserResponse(UserBase):
    user_id : UUID
    is_active: bool
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    user_name: Optional[str]= Field(None, min_length=1, max_length=50)
    password: str | None = Field(default=None, min_length=8)
    class Config:
        extra = "forbid"
    