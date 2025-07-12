import asyncio
import random
from pprint import pprint

from sqlalchemy import select, func, text
from faker import Faker

from db import AsyncSessionLocal
from models import User, Transaction, TransactionType


async def main():
    async with AsyncSessionLocal() as session:
        fake = Faker()

        users = []
        for _ in range(10):
            user = User(
                name=fake.name(),
                email=fake.unique.email()
            )
            users.append(user)
            session.add(user)
        await session.commit()

        transaction_types = list(TransactionType)
        for _ in range(100):
            user = random.choice(users)
            transaction = Transaction(
                user_id=user.id,
                transaction_type=random.choice(transaction_types),
                value=random.randint(-100, 100),
                properties={
                    "description": fake.sentence(),
                    "location": fake.city()
                }
            )
            session.add(transaction)
        await session.commit()

    # Получение статистики 1
    async with AsyncSessionLocal() as session:
        query = (
            select(
                User.email.label("user_email"),
                func.sum(Transaction.value).label("balance"),
                func.max(Transaction.created_at).label("last_transaction_at"),
            )
            .join(Transaction, User.id == Transaction.user_id)
            .group_by(User.email)
            .order_by(text("balance DESC"), User.email.asc())
            .limit(5)
        )
        result = await session.execute(query)
        statistics = result.all()
        pprint(statistics)

    # Получение статистики 2
    async with AsyncSessionLocal() as session:
        subquery = (
            select(
                Transaction.user_id,
                func.sum(Transaction.value).label("balance")
            )
            .group_by(Transaction.user_id)
            .subquery()
        )
        avg_subquery = select(func.avg(subquery.c.balance)).scalar_subquery()
        query = (
            select(
                User.email,
                func.sum(Transaction.value).label("balance"),
                func.count(Transaction.id).label("transactions_count")
            )
            .join(Transaction, User.id == Transaction.user_id)
            .group_by(User.email)
            .having(func.sum(Transaction.value) > avg_subquery)
            .order_by(text("balance"))
            .limit(5)
        )
        result = await session.execute(query)
        statistics = result.all()
        pprint(statistics)

if __name__ == "__main__":
    asyncio.run(main())
