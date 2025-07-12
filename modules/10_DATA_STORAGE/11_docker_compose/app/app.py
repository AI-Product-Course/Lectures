from typing import AsyncGenerator

import sqlalchemy
from fastapi import FastAPI, Body, Depends
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text



# Settings
class AppSettings(BaseSettings):
    DB_HOST: str = Field(default="")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="")
    DB_PASSWORD: str = Field(default="")
    DB_NAME: str = Field(default="")

    @property
    def asyncpg_db_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = AppSettings()

# Database
engine = create_async_engine(
    url=settings.asyncpg_db_dsn,
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# API
app = FastAPI(title="SQL API")


class SQLQueryRequest(BaseModel):
    query: str
    commit: bool

class SQLQueryResponse(BaseModel):
    answer: str

@app.post("/execute", tags=["internal"], response_model=SQLQueryResponse)
async def execute_query(data: SQLQueryRequest = Body(), session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(text(data.query))
        if data.commit:
            await session.commit()
        return SQLQueryResponse(answer=str(result.all()))
    except sqlalchemy.exc.ResourceClosedError:
        return SQLQueryResponse(answer="Operation successfully completed!")
    except sqlalchemy.exc.ProgrammingError as ex:
        return SQLQueryResponse(answer=str(ex))
