from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import Order, OrderStatus, PaymentMethod, Voucher
from schemas.order import OrderCreate, OrderUpdate


async def create_order(db: AsyncSession, data: OrderCreate) -> Order:
    if data.payment_method == PaymentMethod.qtiwallet:
    # Check wallet, deduct balance, create wallet transaction...
        pass
    # TODO: validate voucher, compute discount, etc if needed
    obj = Order(**data.model_dump(exclude_unset=True))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    # Optional: Update used_count of vouchers
    if obj.admin_voucher_id:
        voucher = await db.get(Voucher, obj.admin_voucher_id)
        if voucher:
            voucher.used_count += 1
            db.add(voucher)
    if obj.shop_voucher_id:
        voucher = await db.get(Voucher, obj.shop_voucher_id)
        if voucher:
            voucher.used_count += 1
            db.add(voucher)
    await db.commit()
    return obj

async def get_order(db: AsyncSession, order_id: int) -> Optional[Order]:
    return await db.get(Order, order_id)

async def update_order(db: AsyncSession, data: OrderUpdate) -> Optional[Order]:
    obj = await db.get(Order, data.order_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        if field != "order_id" and value is not None:
            setattr(obj, field, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_order(db: AsyncSession, order_id: int) -> bool:
    obj = await db.get(Order, order_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True

async def list_orders(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Order]:
    result = await db.execute(select(Order).offset(skip).limit(limit))
    return list(result.scalars().all())

async def get_orders_by_user(db: AsyncSession, user_uid: str, skip: int = 0, limit: int = 100) -> List[Order]:
    result = await db.execute(
        select(Order).where(Order.user_uid == user_uid).offset(skip).limit(limit)
    )
    return list(result.scalars().all())

async def get_orders_by_restaurant(db: AsyncSession, restaurant_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
    result = await db.execute(
        select(Order).where(Order.restaurant_id == restaurant_id).offset(skip).limit(limit)
    )
    return list(result.scalars().all())

async def get_orders_by_status(db: AsyncSession, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
    result = await db.execute(
        select(Order).where(Order.status == status).offset(skip).limit(limit)
    )
    return list(result.scalars().all())

async def get_orders_by_shipper(db: AsyncSession, shipper_uid: str, skip: int = 0, limit: int = 100) -> List[Order]:
    result = await db.execute(
        select(Order).where(Order.shipper_uid == shipper_uid).offset(skip).limit(limit)
    )
    return list(result.scalars().all())

