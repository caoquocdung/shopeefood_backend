from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.category import (
    CategoryCreate, CategoryUpdate, CategoryResponse
)
from services.category import (
    create_category, get_category, update_category, delete_category, list_categories
)
from typing import List

router = APIRouter(prefix="/category", tags=["category"])

@router.post("/create", response_model=CategoryResponse)
async def api_create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    obj = await create_category(db, data)
    return obj

@router.get("/detail/{category_id}", response_model=CategoryResponse)
async def api_get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_category(db, category_id)
    if not obj:
        raise HTTPException(404, "Category not found")
    return obj

@router.put("/update", response_model=CategoryResponse)
async def api_update_category(data: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    obj = await update_category(db, data)
    if not obj:
        raise HTTPException(404, "Category not found")
    return obj

@router.delete("/delete/{category_id}", response_model=dict)
async def api_delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_category(db, category_id)
    if not ok:
        raise HTTPException(404, "Category not found")
    return {"detail": "Deleted"}

@router.get("/list", response_model=List[CategoryResponse])
async def api_list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    objs = await list_categories(db, skip, limit)
    return objs
