import os
import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from schemas.user import UserCreate, UserUpdate
from typing import List, Optional

async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    user = User(**user_create.model_dump(exclude_unset=True))
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
        user.email = user_update.email 
    if user_update.name is not None:
        user.name = user_update.name 
    if user_update.phone is not None:
        user.phone = user_update.phone
    if user_update.gender is not None:
        user.gender = user_update.gender
    if user_update.birthday is not None:
        user.birthday = user_update.birthday
    # if user_update.avatar_url is not None:
    #     user.avatar_url = user_update.avatar_url
    if user_update.role is not None:
        user.role = user_update.role
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


AVATAR_DIR = "static/user_avatars"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 3 * 1024 * 1024  # 3MB

def generate_avatar_filename(uid: str, original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    unique = uuid.uuid4().hex
    return f"{uid}_{unique}{ext}"

#TODO user select upload avater, UI request delete avatar and upload avatar after that.

async def upload_user_avatar(
    db: AsyncSession,
    uid: str,
    file: UploadFile
) -> str:
    # Validate type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "File không đúng định dạng ảnh!")
    # Read content
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "Ảnh quá lớn! Tối đa 3MB.")
    os.makedirs(AVATAR_DIR, exist_ok=True)
    filename = generate_avatar_filename(uid, file.filename)
    file_path = os.path.join(AVATAR_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    avatar_url = f"/static/user_avatars/{filename}"
    # Update avatar_url in DB
    user = await db.get(User, uid)
    if not user:
        raise HTTPException(404, "User not found")
    user.avatar_url = avatar_url
    await db.commit()
    await db.refresh(user)
    return avatar_url

async def delete_user_avatar(
    db: AsyncSession,
    uid: str
) -> bool:
    user = await db.get(User, uid)
    if not user or not user.avatar_url:
        return False
    # Xóa file ảnh
    file_path = os.path.join(AVATAR_DIR, os.path.basename(user.avatar_url))
    if os.path.exists(file_path):
        os.remove(file_path)
    # Cập nhật avatar_url trong DB
    user.avatar_url = None
    await db.commit()
    await db.refresh(user)
    return True