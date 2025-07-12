import asyncio
import uuid

from db import AsyncSessionLocal
from models import User


async def main():
    user_id = uuid.uuid4()

    async with AsyncSessionLocal() as session:
        nick = User(id=user_id, name="Nick Smith", email=f"nick@gmail.com")
        session.add(nick)
        await session.commit()

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        print("session.get: ", user)

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        user.name = "Nolan Smith"
        await session.commit()

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        await session.delete(user)
        await session.commit()

        user = await session.get(User, user_id)
        print("session.get: ", user)

if __name__ == "__main__":
    asyncio.run(main())
