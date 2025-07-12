from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models import Voucher
from schemas.voucher import VoucherCreate, VoucherUpdate

async def create_voucher(db: AsyncSession, data: VoucherCreate) -> Voucher:
    obj = Voucher(**data.model_dump(exclude_unset=True))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_voucher(db: AsyncSession, voucher_id: int) -> Optional[Voucher]:
    return await db.get(Voucher, voucher_id)

async def update_voucher(db: AsyncSession, data: VoucherUpdate) -> Optional[Voucher]:
    obj = await db.get(Voucher, data.voucher_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        if field != "voucher_id" and value is not None:
            setattr(obj, field, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_voucher(db: AsyncSession, voucher_id: int) -> bool:
    obj = await db.get(Voucher, voucher_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True

async def list_vouchers(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Voucher]:
    result = await db.execute(select(Voucher).offset(skip).limit(limit))
    return list(result.scalars().all())

async def list_vouchers_by_resid(
    db: AsyncSession, res_uid: str, skip: int = 0, limit: int = 100
) -> List[Voucher]:
    result = await db.execute(
        select(Voucher).where(Voucher.seller_uid == res_uid).offset(skip).limit(limit)
    )
    return list(result.scalars().all())

async def is_voucher_code_unique(
    db: AsyncSession,
    res_uid: int,
    code: str
) -> bool:
    stmt = select(Voucher).where(
        Voucher.seller_uid == res_uid,
        Voucher.code == code
    )

    result = await db.execute(stmt)
    voucher = result.scalar_one_or_none()
    return voucher is None