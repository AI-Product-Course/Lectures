import uuid
import sqlite3
from typing import Annotated

import asyncpg
from fastapi import FastAPI, status, Body, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from passlib.context import CryptContext


DATABASE_DSN = "postgresql://user:password@localhost:5432/my_db"

async def get_db_connection():
    conn: asyncpg.Connection = await asyncpg.connect(DATABASE_DSN)
    try:
        yield conn
    finally:
        if conn:
            await conn.close()


DBConnection = Annotated[asyncpg.Connection, Depends(get_db_connection)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()


@app.exception_handler(asyncpg.PostgresError)
async def sqlite_error_handler(request: Request, exc: asyncpg.PostgresError):
    result = MessageResponse(text=f"Возникла ошибка: {exc}")
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageResponse(BaseModel):
    text: str


class UserCreateRequest(BaseModel):
    name: str = Field(examples=["Admin"])
    username: str = Field(examples=["admin"])
    password: str = Field(examples=["admin"])


class UserCreateResponse(BaseModel):
    id: str
    name: str
    username: str


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
async def register(conn: DBConnection, data: UserCreateRequest = Body()) -> JSONResponse:
    user_id = str(uuid.uuid4())
    hashed_password = pwd_context.hash(data.password)
    await conn.execute(
        "INSERT INTO users (id, name, username, hashed_password) VALUES ($1, $2, $3, $4)",
        user_id, data.name, data.username, hashed_password
    )

    result = UserCreateResponse(id=user_id, name=data.name, username=data.username)
    return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)
