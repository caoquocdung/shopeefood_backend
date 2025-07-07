from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import CartItem
from schemas.cart_item import CartItemCreate, CartItemUpdate

async def add_cart_item(db: AsyncSession, data: CartItemCreate) -> CartItem:
    # Kiểm tra nếu đã có cart_item (user, restaurant, item) thì update quantity
    stmt = select(CartItem).where(
        CartItem.user_uid == data.user_uid,
        CartItem.restaurant_id == data.restaurant_id,
        CartItem.item_id == data.item_id
    )
    result = await db.execute(stmt)
    existing = result.scalars().first()
    if existing:
        existing.quantity += data.quantity
        if data.note:
            existing.note = data.note
        await db.commit()
        await db.refresh(existing)
        return existing
    obj = CartItem(**data.model_dump(exclude_unset=True))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def update_cart_item(db: AsyncSession, data: CartItemUpdate) -> Optional[CartItem]:
    obj = await db.get(CartItem, data.cart_item_id)
    if not obj:
        return None
    if data.quantity is not None:
        obj.quantity = data.quantity
    if data.note is not None:
        obj.note = data.note
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_cart_item(db: AsyncSession, cart_item_id: int) -> bool:
    obj = await db.get(CartItem, cart_item_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True

async def list_cart_items(
    db: AsyncSession, 
    user_uid: str, 
    restaurant_id: Optional[int] = None
) -> List[CartItem]:
    stmt = select(CartItem).where(CartItem.user_uid == user_uid)
    if restaurant_id:
        stmt = stmt.where(CartItem.restaurant_id == restaurant_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def clear_cart(db: AsyncSession, user_uid: str, restaurant_id: Optional[int] = None):
    stmt = select(CartItem).where(CartItem.user_uid == user_uid)
    if restaurant_id:
        stmt = stmt.where(CartItem.restaurant_id == restaurant_id)
    result = await db.execute(stmt)
    items = result.scalars().all()
    for item in items:
        await db.delete(item)
    await db.commit()
