from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import Category
from schemas.category import CategoryCreate, CategoryUpdate

async def create_category(db: AsyncSession, data: CategoryCreate) -> Category:
    obj = Category(**data.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_category(db: AsyncSession, category_id: int) -> Optional[Category]:
    return await db.get(Category, category_id)

async def update_category(db: AsyncSession, data: CategoryUpdate) -> Optional[Category]:
    obj = await db.get(Category, data.category_id)
    if not obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        if field != "category_id" and value is not None:
            setattr(obj, field, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_category(db: AsyncSession, category_id: int) -> bool:
    obj = await db.get(Category, category_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True

async def list_categories(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return list(result.scalars().all())
