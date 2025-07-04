from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.restaurant import (
    RestaurantCreate, RestaurantUpdate, RestaurantResponse
)
from services.restaurant import (
    create_restaurant, delete_restaurant_image, get_restaurant, update_restaurant, delete_restaurant, list_restaurants, upload_restaurant_image
)
from typing import List

router = APIRouter(prefix="/restaurant", tags=["restaurant"])

@router.post("/create", response_model=RestaurantResponse)
async def api_create_restaurant(data: RestaurantCreate, db: AsyncSession = Depends(get_db)):
    obj = await create_restaurant(db, data)
    return obj

@router.get("/detail/{restaurant_id}", response_model=RestaurantResponse)
async def api_get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_restaurant(db, restaurant_id)
    if not obj:
        raise HTTPException(404, "Restaurant not found")
    return obj

@router.put("/update", response_model=RestaurantResponse)
async def api_update_restaurant(data: RestaurantUpdate, db: AsyncSession = Depends(get_db)):
    obj = await update_restaurant(db, data)
    if not obj:
        raise HTTPException(404, "Restaurant not found")
    return obj

@router.delete("/delete/{restaurant_id}", response_model=dict)
async def api_delete_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_restaurant(db, restaurant_id)
    if not ok:
        raise HTTPException(404, "Restaurant not found")
    return {"detail": "Deleted"}

@router.get("/list", response_model=List[RestaurantResponse])
async def api_list_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    objs = await list_restaurants(db, skip, limit)
    return objs

@router.post("/upload_image", response_model=dict)
async def api_upload_restaurant_image(
    restaurant_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a restaurant image. Returns the image URL.
    """
    image_url = await upload_restaurant_image(db, restaurant_id, file)
    return {"image_url": image_url}

@router.delete("/delete_image", response_model=dict)
async def api_delete_restaurant_image(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a restaurant image. Returns success message.
    """
    ok = await delete_restaurant_image(restaurant_id, db)
    if not ok:
        raise HTTPException(404, "Restaurant not found or image not found")
    return {"detail": "Image deleted successfully"}