from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


from models import DiscountType, VoucherStatus

class VoucherCreate(BaseModel):
    code: str
    title: Optional[str] = None
    discount_type: DiscountType
    discount_value: Decimal
    min_order: Optional[Decimal] = None
    max_discount: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
    seller_uid: Optional[int] = None
    status: VoucherStatus = VoucherStatus.active
    created_by_admin: bool = False

class VoucherUpdate(BaseModel):
    voucher_id: int
    title: Optional[str] = None
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[Decimal] = None
    min_order: Optional[Decimal] = None
    max_discount: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
    status: Optional[VoucherStatus] = None

class VoucherResponse(BaseModel):
    voucher_id: int
    code: str
    title: Optional[str]
    discount_type: str
    discount_value: Decimal
    min_order: Optional[Decimal]
    max_discount: Optional[Decimal]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    usage_limit: Optional[int]
    used_count: int
    seller_uid: Optional[int]
    status: str
    created_by_admin: bool 

    class Config:
        from_attributes = True
