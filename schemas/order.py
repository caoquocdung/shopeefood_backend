from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from models import OrderStatus, PaymentMethod

class OrderCreate(BaseModel):
    user_uid: str
    restaurant_id: int
    total_price: Decimal
    address_id: Optional[int] = None
    # delivery_address: Optional[str] = None
    note: Optional[str] = None
    admin_voucher_id: Optional[int] = None
    shop_voucher_id: Optional[int] = None
    payment_method: PaymentMethod = PaymentMethod.cod
    # shipper_uid sẽ được cập nhật khi gán shipper

class OrderUpdate(BaseModel):
    order_id: int
    status: Optional[OrderStatus] = None
    total_price: Optional[Decimal] = None
    address_id: Optional[int] = None
    # delivery_address: Optional[str] = None
    note: Optional[str] = None
    shipper_uid: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None

class OrderResponse(BaseModel):
    order_id: int
    user_uid: str
    restaurant_id: int
    shipper_uid: Optional[str]
    total_price: Decimal
    status: OrderStatus
    address_id: Optional[int]
    # delivery_address: Optional[str]
    admin_voucher_id: Optional[int]
    shop_voucher_id: Optional[int]
    note: Optional[str]
    payment_method: PaymentMethod
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
