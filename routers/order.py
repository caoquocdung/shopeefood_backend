from http.client import HTTPException
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.order import OrderCreate, OrderResponse, OrderUpdate
from services.order import create_order, delete_order, get_order, get_orders_by_restaurant, get_orders_by_shipper, get_orders_by_status, get_orders_by_user, list_orders, update_order


router = APIRouter(prefix="/order", tags=["Order"])

@router.post("/create", response_model=OrderResponse)
async def api_create_order(data: OrderCreate, db: AsyncSession = Depends(get_db)):  
    obj = await create_order(db, data)
    return obj

@router.get("/detail/{order_id}", response_model=OrderResponse)
async def api_get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_order(db, order_id)
    if not obj:
        raise HTTPException(404, "Order not found")
    return obj

@router.put("/update", response_model=OrderResponse)
async def api_update_order(data: OrderUpdate, db: AsyncSession = Depends(get_db)):
    obj = await update_order(db, data)
    if not obj:
        raise HTTPException(404, "Order not found")
    return obj

@router.delete("/delete/{order_id}", response_model=dict)
async def api_delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_order(db, order_id)
    if not ok:
        raise HTTPException(404, "Order not found")
    return {"detail": "Deleted"}

@router.get("/list", response_model=List[OrderResponse])
async def api_list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    objs = await list_orders(db, skip, limit)
    return objs

@router.get("/by_user/{user_uid}", response_model=List[OrderResponse])
async def api_get_orders_by_user(
    user_uid: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all orders made by a specific user.
    """
    objs = await get_orders_by_user(db, user_uid, skip, limit)
    return objs

@router.get("/by_restaurant/{restaurant_id}", response_model=List[OrderResponse])
async def api_get_orders_by_restaurant(
    restaurant_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all orders made for a specific restaurant.
    """
    objs = await get_orders_by_restaurant(db, restaurant_id, skip, limit)
    return objs

@router.get("/by_status/{status}", response_model=List[OrderResponse])
async def api_get_orders_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all orders with a specific status.
    """
    objs = await get_orders_by_status(db, status, skip, limit)
    return objs

@router.get("/by_shipper/{shipper_uid}", response_model=List[OrderResponse])
async def api_get_orders_by_shipper(
    shipper_uid: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all orders assigned to a specific shipper.
    """
    objs = await get_orders_by_shipper(db, shipper_uid, skip, limit)
    return objs

