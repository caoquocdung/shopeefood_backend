from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class OrderItemCreate(BaseModel):
    order_id: int
    item_id: int
    quantity: int = 1
    price: Decimal
    note: Optional[str] = None

class OrderItemUpdate(BaseModel):
    order_item_id: int
    quantity: Optional[int] = None
    price: Optional[Decimal] = None
    note: Optional[str] = None

class OrderItemResponse(BaseModel):
    order_item_id: int
    order_id: int
    item_id: int
    quantity: int
    price: Decimal
    note: Optional[str]

    class Config:
        from_attributes = True
