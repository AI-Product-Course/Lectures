from typing import Annotated

import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends


DATABASE_DSN = "postgresql://user:password@localhost:5432/my_db"

pool = None

async def get_db_connection():
    async with pool.acquire() as conn:
        yield conn

DBConnection = Annotated[asyncpg.Connection, Depends(get_db_connection)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await asyncpg.create_pool(DATABASE_DSN, min_size=3, max_size=9)
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)


@app.get("/test")
async def test(conn: DBConnection):
    result = await conn.fetchval("SELECT 1+1")
    return {"result": result}
