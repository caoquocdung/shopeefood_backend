from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.voucher import (
    VoucherCreate, VoucherUpdate, VoucherResponse
)
from services.voucher import (
    create_voucher, get_voucher, update_voucher, delete_voucher, list_vouchers
)
from typing import List

router = APIRouter(prefix="/voucher", tags=["voucher"])

# TODO để ý VoucherStatus và DiscountType gửi về từ client có thể không đúng với enum trong models 
# class VoucherStatus(enum.Enum):
#     active = 'active'
#     expired = 'expired'
#     disabled = 'disabled'

# class DiscountType(enum.Enum):
#     percentage = "percentage"
#     fixed = "fixed"

@router.post("/create", response_model=VoucherResponse)
async def api_create_voucher(data: VoucherCreate, db: AsyncSession = Depends(get_db)):
    obj = await create_voucher(db, data)
    return obj

@router.get("/detail/{voucher_id}", response_model=VoucherResponse)
async def api_get_voucher(voucher_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_voucher(db, voucher_id)
    if not obj:
        raise HTTPException(404, "Voucher not found")
    return obj

@router.put("/update", response_model=VoucherResponse)
async def api_update_voucher(data: VoucherUpdate, db: AsyncSession = Depends(get_db)):
    obj = await update_voucher(db, data)
    if not obj:
        raise HTTPException(404, "Voucher not found")
    return obj

@router.delete("/delete/{voucher_id}", response_model=dict)
async def api_delete_voucher(voucher_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_voucher(db, voucher_id)
    if not ok:
        raise HTTPException(404, "Voucher not found")
    return {"detail": "Deleted"}

@router.get("/list", response_model=List[VoucherResponse])
async def api_list_vouchers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: AsyncSession = Depends(get_db)
):
    objs = await list_vouchers(db, skip, limit)
    return objs
