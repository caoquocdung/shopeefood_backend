from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from models import RestaurantStatus


# RestaurantCreate: for creating a new restaurant
class RestaurantCreate(BaseModel):
    owner_uid: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    open_time: Optional[datetime] = None
    close_time: Optional[datetime] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[RestaurantStatus] = RestaurantStatus.open  # Default status is active


# RestaurantUpdate: for updating restaurant info
class RestaurantUpdate(BaseModel):
    restaurant_id: int
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_favorite: Optional[bool] = None  # Optional field for favorite status
    open_time: Optional[datetime] = None
    close_time: Optional[datetime] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[RestaurantStatus] = None  # Allow status to be updated, but not required


# RestaurantResponse: for returning restaurant info (all fields, matching model)
class RestaurantResponse(BaseModel):
    restaurant_id: int
    owner_uid: str
    name: str
    address: Optional[str]
    phone: Optional[str]
    is_favorite: Optional[bool] = None
    open_time: Optional[datetime]
    close_time: Optional[datetime]
    description: Optional[str]
    image_url: Optional[str]
    status: Optional[RestaurantStatus]
    rating: Optional[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True