from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.menu_item import (
    MenuItemCreate, MenuItemUpdate, MenuItemResponse,
    MenuItemImageCreate, MenuItemImageResponse
)
from services.menu_item import (
    create_menu_item, get_menu_item, update_menu_item, delete_menu_item,
    list_menu_items,
    add_menu_item_image, delete_menu_item_image, list_menu_item_images,
    upload_menu_image_service, upload_multi_menu_images_service, list_menu_items_by_category, list_menu_items_by_restaurant_id
)
from typing import List

router = APIRouter(prefix="/menu_item", tags=["menu_item"])

# ----- Menu Item -----
@router.post("/create", response_model=MenuItemResponse)
async def api_create_menu_item(data: MenuItemCreate, db: AsyncSession = Depends(get_db)):
    item = await create_menu_item(db, data)
    if not item:
        raise HTTPException(400, "Failed to create menu item")
    return item

@router.get("/detail/{item_id}", response_model=MenuItemResponse)
async def api_get_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_menu_item(db, item_id)
    if not item:
        raise HTTPException(404, "Menu item not found")
    return item

@router.put("/update", response_model=MenuItemResponse)
async def api_update_menu_item(data: MenuItemUpdate, db: AsyncSession = Depends(get_db)):
    item = await update_menu_item(db, data)
    if not item:
        raise HTTPException(404, "Menu item not found")
    return item

@router.delete("/delete/{item_id}", response_model=dict)
async def api_delete_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_menu_item(db, item_id)
    if not ok:
        raise HTTPException(404, "Menu item not found")
    return {"detail": "Deleted"}

@router.get("/list", response_model=List[MenuItemResponse])
async def api_list_menu_items(skip: int = Query(0, ge=0), limit: int = Query(100, gt=0), db: AsyncSession = Depends(get_db)):
    items = await list_menu_items(db, skip, limit)
    return items

@router.get("/menu_items/{category_id}", response_model=List[MenuItemResponse])
async def api_list_menu_items_by_category(
    category_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    items = await list_menu_items_by_category(db, category_id, skip, limit)
    return items

@router.get("/menu_items_by_resid/{restaurant_id}", response_model=List[MenuItemResponse])
async def api_list_menu_items_by_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    items = await list_menu_items_by_restaurant_id(db, restaurant_id)
    return items

# ----- Menu Item Images -----
@router.post("/image/add", response_model=MenuItemImageResponse)
async def api_add_menu_item_image(data: MenuItemImageCreate, db: AsyncSession = Depends(get_db)):
    img = await add_menu_item_image(db, data)
    return img

@router.get("/image/list/{item_id}", response_model=List[MenuItemImageResponse])
async def api_list_menu_item_images(item_id: int, db: AsyncSession = Depends(get_db)):
    imgs = await list_menu_item_images(db, item_id)
    return imgs

@router.delete("/image/delete/{image_id}", response_model=dict)
async def api_delete_menu_item_image(image_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_menu_item_image(db, image_id)
    if not ok:
        raise HTTPException(404, "Image not found")
    return {"detail": "Image deleted"}

@router.post("/image/upload", response_model=MenuItemImageResponse)
async def upload_menu_item_image(
    item_id: int = Form(...),
    is_primary: bool = Form(False),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    img = await upload_menu_image_service(db, item_id, file, is_primary)
    return img


@router.post("/image/upload-multi", response_model=List[MenuItemImageResponse])
async def upload_menu_item_images(
    item_id: int = Form(...),
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    images = await upload_multi_menu_images_service(db, item_id, files)
    return images