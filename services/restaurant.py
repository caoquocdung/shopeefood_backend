from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import Restaurant
from schemas.restaurant import RestaurantCreate, RestaurantUpdate

async def create_restaurant(db: AsyncSession, data: RestaurantCreate) -> Restaurant:
    obj = Restaurant(**data.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_restaurant(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    return await db.get(Restaurant, restaurant_id)

async def update_restaurant(db: AsyncSession, data: RestaurantUpdate) -> Optional[Restaurant]:
    obj = await db.get(Restaurant, data.restaurant_id)
    if not obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        if field != "restaurant_id" and value is not None:
            setattr(obj, field, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_restaurant(db: AsyncSession, restaurant_id: int) -> bool:
    obj = await db.get(Restaurant, restaurant_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True

async def list_restaurants(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Restaurant]:
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    return list(result.scalars().all())
