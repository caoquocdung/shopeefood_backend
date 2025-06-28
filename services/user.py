from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from schemas.user import UserCreate, UserUpdate
from typing import List, Optional

async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    user = User(
        uid=user_create.uid,
        email=user_create.email,
        name=user_create.name,
        phone=user_create.phone,
        role=user_create.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, uid: str) -> Optional[User]:
    return await db.get(User, uid)

async def update_user(db: AsyncSession, user_update: UserUpdate) -> Optional[User]:
    user = await db.get(User, user_update.uid)
    if not user:
        return None
    # Cập nhật các trường nếu có
    if user_update.email is not None:
        user.email = user_update.email # type: ignore
    if user_update.name is not None:
        user.name = user_update.name # type: ignore
    if user_update.phone is not None:
        user.phone = user_update.phone # type: ignore
    if user_update.role is not None:
        user.role = user_update.role # type: ignore
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, uid: str) -> bool:
    user = await db.get(User, uid)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True

async def list_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())
