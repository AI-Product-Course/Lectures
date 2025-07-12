from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from sqlalchemy.orm import joinedload

from db import AsyncSessionLocal
from models import TransactionType, User, Transaction


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


app = FastAPI(title="User API")


class DetailedTransactionSchema(BaseModel):
    id: UUID
    transaction_type: TransactionType
    value: int
    properties: dict
    created_at: datetime

class BalanceResponse(BaseModel):
    balance: int
    count: int
    detailed_transactions: list[DetailedTransactionSchema]


@app.get("/users/{email}/balance", tags=["users"], response_model=BalanceResponse)
async def get_user_balance(email: str, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    query = (
        select(
            User.id,
            func.sum(Transaction.value).label("balance"),
            func.count(Transaction.id).label("count"),
        )
        .join(Transaction, User.id == Transaction.user_id)
        .group_by(User.id)
        .where(User.email == email)
    )
    result = await session.execute(query)
    row = result.fetchone()
    if not row:
        return JSONResponse(content="No user with this email", status_code=status.HTTP_404_NOT_FOUND)

    user_id, balance, count = row

    query = (
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc())
    )
    result = await session.execute(query)
    transactions = result.all()
    return BalanceResponse(
        balance=balance,
        count=count,
        detailed_transactions=[
            DetailedTransactionSchema(**t[0].__dict__)
            for t in transactions
        ]
    )


@app.get("/users/{email}/balance2", tags=["users"], response_model=BalanceResponse)
async def get_user_balance(email: str, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    query = (
        select(User)
        .where(User.email == email)
        .options(joinedload(User.transactions))
    )
    result = await session.execute(query)
    row = result.unique().fetchone()
    if not row:
        return JSONResponse(content="No user with this email", status_code=status.HTTP_404_NOT_FOUND)

    user = row[0]
    return BalanceResponse(
        balance=sum(t.value for t in user.transactions),
        count=len(user.transactions),
        detailed_transactions=[
            DetailedTransactionSchema(**t.__dict__)
            for t in user.transactions
        ]
    )
