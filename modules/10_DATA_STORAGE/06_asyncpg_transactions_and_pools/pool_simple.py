import asyncio

import asyncpg


DATABASE_DSN = "postgresql://user:password@localhost:5432/my_db"


async def execute_query(pool: asyncpg.Pool, query: str):
    async with pool.acquire() as connection:
        return await connection.fetchval(query)

async def main():
    query = "SELECT 1+1"
    async with asyncpg.create_pool(DATABASE_DSN, min_size=3, max_size=9) as pool:
        await asyncio.gather(execute_query(pool, query), execute_query(pool, query))

asyncio.run(main())