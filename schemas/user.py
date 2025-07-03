from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from models import UserStatus, UserRole

class UserProfileRequest(BaseModel):
    uid: str


# UserCreate: for creating a new user (uid, email required, others optional)
class UserCreate(BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    avatar_url: Optional[str] = None
    role: UserRole = UserRole.customer  


# UserUpdate: for updating user info (all fields optional except uid)
class UserUpdate(BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    avatar_url: Optional[str] = None
    status: Optional[UserStatus] = UserStatus.active
    role: UserRole = UserRole.customer  


# UserResponse: for returning user info (all fields, matching model)
class UserResponse(BaseModel):
    uid: str
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    birthday: Optional[datetime]
    avatar_url: Optional[str]
    status: Optional[str]
    role: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
