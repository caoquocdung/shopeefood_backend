from pydantic import BaseModel
from typing import Optional
from models import RestaurantStatus


# RestaurantCreate: for creating a new restaurant
class RestaurantCreate(BaseModel):
    owner_uid: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[RestaurantStatus] = RestaurantStatus.active  # Default status is active


# RestaurantUpdate: for updating restaurant info
class RestaurantUpdate(BaseModel):
    restaurant_id: int
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None
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
    open_time: Optional[str]
    close_time: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    status: Optional[RestaurantStatus]
    rating: Optional[float]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True