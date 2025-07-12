import uuid
import sqlite3
from typing import Literal, Annotated
from datetime import datetime

from fastapi import FastAPI, status, Body, Path, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from passlib.context import CryptContext


DATABASE = "project.db"

def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        yield conn
    finally:
        if conn:
            conn.close()


DBConnection = Annotated[sqlite3.Connection, Depends(get_db_connection)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()


@app.exception_handler(sqlite3.Error)
async def sqlite_error_handler(request: Request, exc: sqlite3.Error):
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
def register(conn: DBConnection, data: UserCreateRequest = Body()) -> JSONResponse:
    try:
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
        raise ex
