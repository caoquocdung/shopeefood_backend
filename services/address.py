from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.address import AddressCreate, AddressUpdate
from models import Address

async def create_address(
        db: AsyncSession,
        address_create: AddressCreate
        ) -> Address:
    # Lấy các địa chỉ đã có
    result = await db.execute(select(Address).where(Address.user_uid == address_create.user_uid))
    existing_addresses = result.scalars().all()

    # Kiểm tra trùng địa chỉ
    if any(addr.address == address_create.address for addr in existing_addresses):
        raise HTTPException(status_code=400, detail="Address already exists for this user")
    
    # Nếu là default, unset các địa chỉ khác
    if address_create.is_default and existing_addresses:
        await db.execute(
            update(Address)
            .where(Address.user_uid == address_create.user_uid)
            .values(is_default=False)
        )
        await db.commit()

    # Nếu là địa chỉ đầu tiên, auto là default
    if not existing_addresses:
        address_create.is_default = True

    # Tạo mới
    address = Address(
        user_uid=address_create.user_uid,
        receiver=address_create.receiver,
        phone=address_create.phone,
        address=address_create.address,
        latitude=address_create.latitude,
        longitude=address_create.longitude,
        is_default=address_create.is_default
    )
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address

async def get_address(db: AsyncSession, address_id: int) -> Optional[Address]:
    return await db.get(Address, address_id)

async def update_address(db: AsyncSession, address_update: AddressUpdate) -> Optional[Address]:
    address = await db.get(Address, address_update.address_id)
    if not address:
        return None
    
    if address_update.receiver is not None:
        address.receiver = address_update.receiver 
    if address_update.phone is not None:
        address.phone = address_update.phone 
    # Chỉ cập nhật địa chỉ nếu có thay đổi
    # Nếu không có thay đổi thì không cần cập nhật
    # TODO
    if address_update.address is not None:
        address.address = address_update.address 
    if address_update.latitude is not None:
        address.latitude = address_update.latitude 
    if address_update.longitude is not None:
        address.longitude = address_update.longitude 
    if address_update.is_default is not None:
        address.is_default = address_update.is_default

    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address

async def delete_address(db: AsyncSession, address_id: int) -> bool:
    address = await db.get(Address, address_id)
    if not address:
        return False
    await db.delete(address)
    await db.commit()
    return True

async def list_addresses_of_user(db: AsyncSession, uid: str, skip: int = 0, limit: int = 100) -> list[Address]:
    result = await db.execute(
        select(Address).where(Address.user_uid == uid).offset(skip).limit(limit)
    )
    return list(result.scalars().all())