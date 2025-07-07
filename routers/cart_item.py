from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.cart_item import CartItemCreate, CartItemUpdate, CartItemResponse
from services.cart_item import (
    add_cart_item, update_cart_item, delete_cart_item, list_cart_items, clear_cart
)
from typing import List

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add", response_model=CartItemResponse)
async def api_add_cart_item(
    data: CartItemCreate,
    db: AsyncSession = Depends(get_db)
):
    obj = await add_cart_item(db, data)
    return obj

@router.put("/update", response_model=CartItemResponse)
async def api_update_cart_item(
    data: CartItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    obj = await update_cart_item(db, data)
    if not obj:
        raise HTTPException(404, "Cart item not found")
    return obj

@router.delete("/delete/{cart_item_id}", response_model=dict)
async def api_delete_cart_item(
    cart_item_id: int,
    db: AsyncSession = Depends(get_db)
):
    ok = await delete_cart_item(db, cart_item_id)
    if not ok:
        raise HTTPException(404, "Cart item not found")
    return {"detail": "Deleted"}

@router.get("/list", response_model=List[CartItemResponse])
async def api_list_cart_items(
    user_uid: str = Query(...),
    restaurant_id: int = Query(None),
    db: AsyncSession = Depends(get_db)
):
    objs = await list_cart_items(db, user_uid, restaurant_id)
    return objs

@router.delete("/clear", response_model=dict)
async def api_clear_cart(
    user_uid: str = Query(...),
    restaurant_id: int = Query(None),
    db: AsyncSession = Depends(get_db)
):
    await clear_cart(db, user_uid, restaurant_id)
    return {"detail": "Cart cleared"}
