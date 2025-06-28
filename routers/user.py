from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.user import (
    UserProfileRequest, UserCreate, UserUpdate, UserResponse
)
from services.user import (
    create_user, get_user, update_user, delete_user, list_users
)
from typing import List

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=UserResponse)
async def api_create_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    # Có thể check user tồn tại trước nếu muốn
    existing = await get_user(db, user_create.uid)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user = await create_user(db, user_create)
    return user

@router.post("/profile", response_model=UserResponse)
async def api_get_profile(req: UserProfileRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, req.uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/update", response_model=UserResponse)
async def api_update_user(user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await update_user(db, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/delete/{uid}", response_model=dict)
async def api_delete_user(uid: str, db: AsyncSession = Depends(get_db)):
    ok = await delete_user(db, uid)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

@router.get("/list", response_model=List[UserResponse])
async def api_list_users(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, gt=0), 
    db: AsyncSession = Depends(get_db)
):
    users = await list_users(db, skip=skip, limit=limit)
    return users
