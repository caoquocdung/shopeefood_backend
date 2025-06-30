import os
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update
from typing import List, Optional
from models import MenuItem, MenuItemImage
from schemas.menu_item import (
    MenuItemCreate, MenuItemUpdate,
    MenuItemImageCreate
)
from fastapi import HTTPException, UploadFile

# CRUD MenuItem

async def create_menu_item(db: AsyncSession, data: MenuItemCreate) -> MenuItem:
    item = MenuItem(**data.model_dump(exclude_unset=True))
    db.add(item)
    await db.commit()
    await db.refresh(item)

    result = await db.execute(
        select(MenuItem).options(selectinload(MenuItem.images)).where(MenuItem.item_id == item.item_id)
    )
    return result.scalars().first()

async def get_menu_item(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    return await db.get(MenuItem, item_id, options=[selectinload(MenuItem.images)])

async def update_menu_item(db: AsyncSession, data: MenuItemUpdate) -> Optional[MenuItem]:
    item = await db.get(MenuItem, data.item_id)
    if not item:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        if field != "item_id" and value is not None:
            setattr(item, field, value)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    result = await db.execute(
        select(MenuItem).options(selectinload(MenuItem.images)).where(MenuItem.item_id == item.item_id)
    )
    item = result.scalars().first()
    if not item:
        return None
    return item

async def delete_menu_item(db: AsyncSession, item_id: int) -> bool:
    item = await db.get(MenuItem, item_id)
    if not item:
        return False
    await db.delete(item)
    await db.commit()
    return True

async def list_menu_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[MenuItem]:
    result = await db.execute(select(MenuItem).options(selectinload(MenuItem.images)).offset(skip).limit(limit))
    return list(result.scalars().all())

async def list_menu_items_by_category(db, category_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(MenuItem).options(selectinload(MenuItem.images)).where(MenuItem.category_id == category_id).offset(skip).limit(limit)
    )
    return list(result.scalars().all())

# CRUD MenuItemImage

async def add_menu_item_image(db: AsyncSession, data: MenuItemImageCreate) -> MenuItemImage:
    # Nếu set is_primary = True, unset các ảnh primary khác
    if data.is_primary:
        await db.execute(
            update(MenuItemImage)
            .where(MenuItemImage.item_id == data.item_id)
            .values(is_primary=False)
        )
        await db.commit()
    img = MenuItemImage(**data.dict())
    db.add(img)
    await db.commit()
    await db.refresh(img)
    return img

async def delete_menu_item_image(db: AsyncSession, image_id: int) -> bool:
    img = await db.get(MenuItemImage, image_id)
    if not img:
        return False
    await db.delete(img)
    await db.commit()
    return True

async def list_menu_item_images(db: AsyncSession, item_id: int) -> List[MenuItemImage]:
    result = await db.execute(select(MenuItemImage).where(MenuItemImage.item_id == item_id))
    return list(result.scalars().all())

UPLOAD_DIR = "static/menu_images"
MAX_SIZE = 3 * 1024 * 1024     # 3MB
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}

def generate_image_filename(item_id: int, original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    unique = uuid.uuid4().hex
    return f"{item_id}_{unique}{ext}"


async def upload_menu_image_service(
    db: AsyncSession,
    item_id: int,
    file: UploadFile,
    is_primary: bool = False
) -> MenuItemImage:
    # Validate type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"File {file.filename} is not an allowed image type!")
    # Read content
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, f"File {file.filename} is too large! Max 3MB.")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    if not file.filename:
        raise HTTPException(400, "Uploaded file must have a filename.")    
    filename = generate_image_filename(item_id, file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    image_url = f"/static/menu_images/{filename}"

    # Nếu là primary, unset các ảnh primary cũ của item này
    if is_primary:
        await db.execute(
            update(MenuItemImage)
            .where(MenuItemImage.item_id == item_id)
            .values(is_primary=False)
        )
        await db.commit()
    img = MenuItemImage(
        item_id=item_id,
        image_url=image_url,
        is_primary=is_primary
    )
    db.add(img)
    await db.commit()
    await db.refresh(img)
    return img

async def upload_multi_menu_images_service(
    db: AsyncSession,
    item_id: int,
    files: List[UploadFile],
    is_primary: bool = False
) -> List[MenuItemImage]:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    results = []
    # Nếu có ít nhất 1 ảnh is_primary, unset tất cả primary cũ (chỉ 1 lần)
    set_primary = is_primary or any(is_primary for _ in files)
    if set_primary:
        await db.execute(
            update(MenuItemImage)
            .where(MenuItemImage.item_id == item_id)
            .values(is_primary=False)
        )
        await db.commit()
    for i, file in enumerate(files):
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(400, f"File {file.filename} is not an allowed image type!")
        content = await file.read()
        if len(content) > MAX_SIZE:
            raise HTTPException(400, f"File {file.filename} is too large! Max 3MB.")
        if not file.filename:
            raise HTTPException(400, "Uploaded file must have a filename.")
        filename = generate_image_filename(item_id, file.filename)
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(content)
        image_url = f"/static/menu_images/{filename}"
        img = MenuItemImage(
            item_id=item_id,
            image_url=image_url,
            is_primary=is_primary if i == 0 else False  # Có thể chỉnh lại logic nếu muốn cho FE tự chọn primary
        )
        db.add(img)
        results.append(img)
    await db.commit()
    for img in results:
        await db.refresh(img)
    return results