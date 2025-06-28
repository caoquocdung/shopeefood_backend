from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas.address import (
    AddressCreate, AddressUpdate, AddressResponse
)
from services.address import (
    create_address, get_address, update_address, delete_address, list_addresses_of_user
)
from typing import List

router = APIRouter(prefix="/address", tags=["address"])

@router.post("/create", response_model=AddressResponse)
async def api_create_address(address_create: AddressCreate, db: AsyncSession = Depends(get_db)):
    existing_addresses = await list_addresses_of_user(db, address_create.uid)
    if existing_addresses and any(addr.uid == address_create.uid for addr in existing_addresses):
        raise HTTPException(status_code=400, detail="Address already exists for this user")
    
    # If the address is default, set all other addresses to not default
    # Nhớ tạo nút để chỉ định địa chỉ mặc định
    if address_create.is_default and existing_addresses:
        for addr in existing_addresses:
            if addr.is_default:
                addr.is_default = False
                db.add(addr)
        await db.commit()
        await db.refresh(existing_addresses)

    # Nếu không có địa chỉ nào thì địa chỉ mới sẽ là mặc định
    if not existing_addresses and address_create.is_default:
        address_create.is_default = True

    address = await create_address(db, address_create)
    return address


@router.get("/{address_id}", response_model=AddressResponse)
async def api_get_address(address_id: int, db: AsyncSession = Depends(get_db)):
    address = await get_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.put("/update", response_model=AddressResponse)
async def api_update_address(address_update: AddressUpdate, db: AsyncSession = Depends(get_db)):
    address = await update_address(db, address_update)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.delete("/{address_id}", response_model=dict)
async def api_delete_address(address_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_address(db, address_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"detail": "Address deleted"}

@router.get("/list/{uid}", response_model=List[AddressResponse])
async def api_list_addresses_of_user(uid: str, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    addresses = await list_addresses_of_user(db, uid, skip=skip, limit=limit)
    return addresses

@router.get("/default/{uid}", response_model=AddressResponse)
async def api_get_default_address(uid: str, db: AsyncSession = Depends(get_db)):
    addresses = await list_addresses_of_user(db, uid)
    default_address = next((addr for addr in addresses if addr.is_default), None)
    if not default_address:
        raise HTTPException(status_code=404, detail="Default address not found")
    return default_address