from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.order_item import (
    OrderItemCreate, OrderItemUpdate, OrderItemResponse
)
from services.order_item import (
    create_order_item, get_order_item, update_order_item, delete_order_item, list_order_items
)
from typing import List

router = APIRouter(prefix="/order_item", tags=["order_item"])

@router.post("/create", response_model=OrderItemResponse)
async def api_create_order_item(data: OrderItemCreate, db: AsyncSession = Depends(get_db)):
    obj = await create_order_item(db, data)
    return obj

@router.get("/detail/{order_item_id}", response_model=OrderItemResponse)
async def api_get_order_item(order_item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_order_item(db, order_item_id)
    if not obj:
        raise HTTPException(404, "Order item not found")
    return obj

@router.put("/update", response_model=OrderItemResponse)
async def api_update_order_item(data: OrderItemUpdate, db: AsyncSession = Depends(get_db)):
    obj = await update_order_item(db, data)
    if not obj:
        raise HTTPException(404, "Order item not found")
    return obj

@router.delete("/delete/{order_item_id}", response_model=dict)
async def api_delete_order_item(order_item_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_order_item(db, order_item_id)
    if not ok:
        raise HTTPException(404, "Order item not found")
    return {"detail": "Deleted"}

@router.get("/list", response_model=List[OrderItemResponse])
async def api_list_order_items(
    order_id: int = Query(None),
    db: AsyncSession = Depends(get_db)
):
    objs = await list_order_items(db, order_id)
    return objs

@router.get("/list_by_order_id/{order_id}", response_model=List[OrderItemResponse])
async def api_get_order_items_by_order_id(order_id: int, db: AsyncSession = Depends(get_db)):
    objs = await list_order_items(db, order_id)
    if not objs:
        raise HTTPException(404, "No order items found for this order")
    return objs