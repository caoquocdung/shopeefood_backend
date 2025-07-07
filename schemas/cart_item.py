from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CartItemCreate(BaseModel):
    user_uid: str
    restaurant_id: int
    item_id: int
    quantity: int = 1
    note: Optional[str] = None

class CartItemUpdate(BaseModel):
    cart_item_id: int
    quantity: Optional[int] = None
    note: Optional[str] = None

class CartItemResponse(BaseModel):
    cart_item_id: int
    user_uid: str
    restaurant_id: int
    item_id: int
    quantity: int
    note: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
