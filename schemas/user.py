from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserProfileRequest(BaseModel):
    uid: str

class UserCreate(BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "customer"

class UserUpdate(BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    # avatar_url: Optional[str] = None
    role: Optional[str] = "customer"

class UserResponse(BaseModel):
    uid: str
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    birthday: Optional[datetime]
    avatar_url: Optional[str]
    role: Optional[str]

    class Config:
        from_attributes = True
