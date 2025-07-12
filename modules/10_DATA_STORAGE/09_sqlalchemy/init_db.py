import asyncio

from db import engine
from models import Base


async def main():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

if __name__ == "__main__":
    asyncio.run(main())
