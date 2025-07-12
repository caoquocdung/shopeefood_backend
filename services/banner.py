import os
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import Banner
from schemas.banner import BannerCreate, BannerUpdate

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 3 * 1024 * 1024  # 3MB
UPLOAD_DIR = "static/banners"


def generate_banner_filename(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    unique = uuid.uuid4().hex
    return f"banner_{unique}{ext}"


async def upload_banner_image(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "File is not an allowed image type!")
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "Image is too large! Max 3MB.")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = generate_banner_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return f"/static/banners/{filename}"


async def create_banner(db: AsyncSession, data: BannerCreate) -> Banner:
    obj = Banner(**data.model_dump(exclude_unset=True))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_banner(db: AsyncSession, banner_id: int) -> Optional[Banner]:
    return await db.get(Banner, banner_id)


async def update_banner(db: AsyncSession, data: BannerUpdate) -> Optional[Banner]:
    obj = await db.get(Banner, data.banner_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        if field != "banner_id" and value is not None:
            setattr(obj, field, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_banner(db: AsyncSession, banner_id: int) -> bool:
    obj = await db.get(Banner, banner_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def list_banners(db: AsyncSession, status: Optional[str] = None) -> List[Banner]:
    stmt = select(Banner)
    if status:
        stmt = stmt.where(Banner.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())
