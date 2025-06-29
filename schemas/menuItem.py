from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile

class MenuItemCreateRequest(BaseModel):
    restaurant_id: int
    category_id: int
    name: str
    description: Optional[str] = None
    price: float

class MenuItemImageUpload(BaseModel):
    item_id: int
    is_primary: bool = False
    sort_order: int = 1

class MenuItemResponse(BaseModel):
    item_id: int
    restaurant_id: int
    category_id: int
    name: str
    description: Optional[str] = None
    price: float
    image_urls: List[str] = []

    class Config:
        from_attributes = True
