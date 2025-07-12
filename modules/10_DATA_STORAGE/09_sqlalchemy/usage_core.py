import asyncio
import uuid

from sqlalchemy import select, insert, update, delete

from db import AsyncSessionLocal
from models import User


async def main():
    user_id = uuid.uuid4()

    # Добавление новой записи
    async with AsyncSessionLocal() as session:
        stmt = insert(User).values(
            id=user_id,
            name="John Smith",
            email="john@gmail.com"
        )
        await session.execute(stmt)
        await session.commit()

    # Получение записи по первичному ключу
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one()
        print("SELECT: ", user)

    # Обновление записи
    async with AsyncSessionLocal() as session:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(name="Jake Smith")
        )
        await session.execute(stmt)
        await session.commit()

        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.all()
        print("SELECT после UPDATE: ", user)

    # Удаление записи
    async with AsyncSessionLocal() as session:
        stmt = delete(User).where(User.id == user_id)
        await session.execute(stmt)
        await session.commit()

        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        print("SELECT после DELETE: ", user)


if __name__ == "__main__":
    asyncio.run(main())
