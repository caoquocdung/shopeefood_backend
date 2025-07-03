from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import Category
from schemas.category import CategoryCreate, CategoryUpdate

import os
from fastapi import HTTPException, UploadFile
import uuid

async def create_category(db: AsyncSession, data: CategoryCreate) -> Category:
    obj = Category(**data.model_dump(exclude_unset=True))
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
    for field, value in data.model_dump(exclude_unset=True).items():
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


CATEGORY_IMAGE_DIR = "static/category_images"
ALLOWED_CATEGORY_IMG_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_CATEGORY_IMG_SIZE = 3 * 1024 * 1024  # 3MB

def generate_category_image_filename(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    unique = uuid.uuid4().hex
    return f"category_{unique}{ext}"

async def upload_category_image(
        db: AsyncSession,
        category_id: int,
        file: UploadFile) -> str:
    # Validate type
    if file.content_type not in ALLOWED_CATEGORY_IMG_TYPES:
        raise HTTPException(400, "File không đúng định dạng ảnh!")
    # Read content
    content = await file.read()
    if len(content) > MAX_CATEGORY_IMG_SIZE:
        raise HTTPException(400, "Ảnh quá lớn! Tối đa 3MB.")
    os.makedirs(CATEGORY_IMAGE_DIR, exist_ok=True)
    filename = generate_category_image_filename(file.filename)
    file_path = os.path.join(CATEGORY_IMAGE_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    image_url = f"/static/category_image/{filename}"
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    category.image_url = image_url  # Update the image URL in the database
    await db.commit()
    await db.refresh(category)
    return image_url

async def delete_category_image(category_id: int, db: AsyncSession) -> bool:
    category = await db.get(Category, category_id)
    if not category or not category.image_url:
        return False
    image_path = os.path.join(CATEGORY_IMAGE_DIR, os.path.basename(category.image_url))
    if os.path.exists(image_path):
        os.remove(image_path)
    category.image_url = None  # Clear the image URL in the database
    await db.commit()
    await db.refresh(category)
    return True
