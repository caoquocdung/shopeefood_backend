from http.client import HTTPException
import os
import uuid
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import Restaurant
from schemas.restaurant import RestaurantCreate, RestaurantUpdate

async def create_restaurant(db: AsyncSession, data: RestaurantCreate) -> Restaurant:
    obj = Restaurant(**data.model_dump(exclude_unset=True))
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
    for field, value in data.model_dump(exclude_unset=True).items():
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

RESTAURANT_IMAGE_DIR = "static/restaurant_images"
ALLOWED_RESTAURANT_IMG_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_RESTAURANT_IMG_SIZE = 3 * 1024 * 1024  # 3MB    

def generate_restaurant_image_filename(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    unique = uuid.uuid4().hex
    return f"restaurant_{unique}{ext}"

async def upload_restaurant_image(
        db: AsyncSession,
        restaurant_id: int,
        file: UploadFile) -> str:
    # Validate type
    if file.content_type not in ALLOWED_RESTAURANT_IMG_TYPES:
        raise HTTPException(400, "Invalid image type")
    # Validate sizecontent = await file.read()
    content = await file.read()
    if not content:
        raise HTTPException(400, "Empty file")
    # Check size
    if len(content) > MAX_RESTAURANT_IMG_SIZE:
        raise HTTPException(400, "Image size exceeds limit")
    # Generate filename
    os.makedirs(RESTAURANT_IMAGE_DIR, exist_ok=True)
    if not file.filename:
        raise HTTPException(400, "Uploaded file must have a filename.")
    filename = generate_restaurant_image_filename(file.filename)
    
    file_path = os.path.join(RESTAURANT_IMAGE_DIR, filename)
    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())
    # Update restaurant image URL
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(404, "Restaurant not found")
    restaurant.image_url = f"/static/restaurant_images/{filename}"
    db.add(restaurant)
    await db.commit()
    await db.refresh(restaurant)

    return restaurant.image_url

async def delete_restaurant_image(restaurant_id: int, db: AsyncSession) -> bool:
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant or not restaurant.image_url:
        return False
    # Delete image file from disk
    image_path = os.path.join(RESTAURANT_IMAGE_DIR, os.path.basename(restaurant.image_url))
    if os.path.exists(image_path):
        os.remove(image_path)
    # Clear image URL in database
    restaurant.image_url = None
    await db.commit()
    await db.refresh(restaurant)
    return True