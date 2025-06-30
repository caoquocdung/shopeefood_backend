from pydantic import BaseModel
from typing import Optional

class RestaurantCreate(BaseModel):
    owner_uid: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None
    status: Optional[str] = "open"

class RestaurantUpdate(BaseModel):
    restaurant_id: int
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None
    status: Optional[str] = None

class RestaurantResponse(BaseModel):
    restaurant_id: int
    owner_uid: str
    name: str
    address: Optional[str]
    phone: Optional[str]
    open_time: Optional[str]
    close_time: Optional[str]
    status: Optional[str]

    class Config:
        from_attributes = True