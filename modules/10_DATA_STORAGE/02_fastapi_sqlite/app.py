import uuid
import sqlite3
from typing import Literal
from datetime import datetime

from fastapi import FastAPI, status, Body, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from passlib.context import CryptContext


DATABASE = "project.db"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()


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
def register(data: UserCreateRequest = Body()) -> JSONResponse:
    conn = None
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            user_id = str(uuid.uuid4())
            hashed_password = pwd_context.hash(data.password)
            cursor.execute(
                "INSERT INTO users (id, name, username, hashed_password) VALUES (?, ?, ?, ?)",
                (user_id, data.name, data.username, hashed_password)
            )
            conn.commit()

            result = UserCreateResponse(id=user_id, name=data.name, username=data.username)
            return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)
    except sqlite3.Error as ex:
        if conn:
            conn.rollback()
        result = MessageResponse(text=f"Возникла ошибка: {ex}")
        return JSONResponse(content=result.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        if conn:
            conn.close()


class TransactionCreateRequest(BaseModel):
    transaction_type: Literal["chat", "top_up"]
    value: int


@app.post("/users/{user_id}/transactions", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def create_transaction(
    user_id: str = Path(),
    data: TransactionCreateRequest = Body(),
) -> JSONResponse:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            result = MessageResponse(text="Пользователь не существует")
            return JSONResponse(content=result.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        transaction_id = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO transactions 
            (id, user_id, transaction_type, value) 
            VALUES (?, ?, ?, ?)""",
            (transaction_id, user_id, data.transaction_type, data.value)
        )
        conn.commit()

        result = MessageResponse(text="Транзакция успешно добавлена")
        return JSONResponse(content=result.model_dump(), status_code=status.HTTP_201_CREATED)


class BalanceResponse(BaseModel):
    current_value: int
    transaction_count: int
    last_changed_at: datetime | None


@app.get("/users/{user_id}/balance")
def get_balance(user_id: str):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return JSONResponse(content=MessageResponse(text="Пользователь не существует").model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        cursor.execute("SELECT COALESCE(SUM(value), 0), COUNT(*), MAX(created_at) FROM transactions WHERE user_id = ?", (user_id,))
        balance, count, last_datetime = cursor.fetchone()
        result = BalanceResponse(current_value=balance, transaction_count=count, last_changed_at=last_datetime)

        return JSONResponse(content=result.model_dump())
