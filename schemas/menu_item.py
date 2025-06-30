from pydantic import BaseModel
from typing import List, Optional

# ----- Menu Item Image -----
class MenuItemImageCreate(BaseModel):
    item_id: int
    image_url: str
    is_primary: Optional[bool] = False

class MenuItemImageResponse(BaseModel):
    image_id: int
    item_id: int
    image_url: str
    is_primary: bool

    class Config:
        from_attributes = True

# ----- Menu Item -----
class MenuItemCreate(BaseModel):
    restaurant_id: int
    category_id: int
    name: str
    description: Optional[str] = None
    price: float
    available: Optional[bool] = True

class MenuItemUpdate(BaseModel):
    item_id: int
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    available: Optional[bool]

class MenuItemResponse(BaseModel):
    item_id: int
    restaurant_id: int
    category_id: int
    name: str
    description: Optional[str]
    price: float
    available: bool
    images: List[MenuItemImageResponse] = []

    class Config:
        from_attributes = True
