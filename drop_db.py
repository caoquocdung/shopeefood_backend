import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models import Base  # import Base từ models.py
from config import DATABASE_URL

async def drop_all():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(drop_all())
