from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.banner import BannerCreate, BannerUpdate, BannerResponse
from services.banner import (
    create_banner,
    get_banner,
    update_banner,
    delete_banner,
    list_banners,
    upload_banner_image
)
from typing import List, Optional

router = APIRouter(prefix="/banner", tags=["banner"])

@router.post("/create", response_model=BannerResponse)
async def api_create_banner(
    data: BannerCreate,
    db: AsyncSession = Depends(get_db)
):
    obj = await create_banner(db, data)
    return obj

@router.get("/detail/{banner_id}", response_model=BannerResponse)
async def api_get_banner(
    banner_id: int,
    db: AsyncSession = Depends(get_db)
):
    obj = await get_banner(db, banner_id)
    if not obj:
        raise HTTPException(404, "Banner not found")
    return obj

@router.put("/update", response_model=BannerResponse)
async def api_update_banner(
    data: BannerUpdate,
    db: AsyncSession = Depends(get_db)
):
    obj = await update_banner(db, data)
    if not obj:
        raise HTTPException(404, "Banner not found")
    return obj

@router.delete("/delete/{banner_id}", response_model=dict)
async def api_delete_banner(
    banner_id: int,
    db: AsyncSession = Depends(get_db)
):
    ok = await delete_banner(db, banner_id)
    if not ok:
        raise HTTPException(404, "Banner not found")
    return {"detail": "Deleted"}

@router.get("/list", response_model=List[BannerResponse])
async def api_list_banners(
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    objs = await list_banners(db, status)
    return objs

@router.post("/upload_img")
async def api_upload_banner_img(
    file: UploadFile = File(...)
):
    url = await upload_banner_image(file)
    return {"image_url": url}
