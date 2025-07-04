from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import OrderItem
from schemas.order_item import OrderItemCreate, OrderItemUpdate

async def create_order_item(db: AsyncSession, data: OrderItemCreate) -> OrderItem:
    obj = OrderItem(**data.model_dump(exclude_unset=True))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_order_item(db: AsyncSession, order_item_id: int) -> Optional[OrderItem]:
    return await db.get(OrderItem, order_item_id)

async def update_order_item(db: AsyncSession, data: OrderItemUpdate) -> Optional[OrderItem]:
    obj = await db.get(OrderItem, data.order_item_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        if field != "order_item_id" and value is not None:
            setattr(obj, field, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_order_item(db: AsyncSession, order_item_id: int) -> bool:
    obj = await db.get(OrderItem, order_item_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True

async def list_order_items(db: AsyncSession, order_id: int = None) -> List[OrderItem]:
    stmt = select(OrderItem)
    if order_id:
        stmt = stmt.where(OrderItem.order_id == order_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_order_items_by_order_id(db: AsyncSession, order_id: int) -> List[OrderItem]:
    stmt = select(OrderItem).where(OrderItem.order_id == order_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

