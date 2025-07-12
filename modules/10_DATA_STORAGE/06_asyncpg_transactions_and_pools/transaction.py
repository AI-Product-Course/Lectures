import uuid
import asyncio

import asyncpg



DATABASE_DSN = "postgresql://user:password@localhost:5432/my_db"


async def wrong_move_tokens(from_user_id: str, to_user_id: str, value: int):
    conn: asyncpg.Connection = await asyncpg.connect(DATABASE_DSN)
    try:
        t1 = str(uuid.uuid4())
        t2 = str(uuid.uuid4())
        await conn.execute("INSERT INTO transactions (id, user_id, transaction_type, value) VALUES ($1, $2, $3, $4)", t1, from_user_id, "u2u", -value)
        await conn.execute("INSERT INTO transactions (id, user_id, transaction_type, value) VALUES ($1, $2, $3, $4)", t2, to_user_id, "u2u", value)
    finally:
        if conn:
            await conn.close()


async def one_operation_move_tokens(from_user_id: str, to_user_id: str, value: int):
    conn: asyncpg.Connection = await asyncpg.connect(DATABASE_DSN)
    try:
        t1 = str(uuid.uuid4())
        t2 = str(uuid.uuid4())
        await conn.executemany(
            "INSERT INTO transactions (id, user_id, transaction_type, value) VALUES ($1, $2, $3, $4)",
            [(t1, from_user_id, "u2u", -value), (t2, to_user_id, "u2u", value)]
        )
    finally:
        if conn:
            await conn.close()


async def transaction_move_tokens(from_user_id: str, to_user_id: str, value: int):
    conn: asyncpg.Connection = await asyncpg.connect(DATABASE_DSN)
    try:
        t1 = str(uuid.uuid4())
        t2 = str(uuid.uuid4())
        async with conn.transaction():
            await conn.execute(
                "INSERT INTO transactions (user_id, transaction_type, value) VALUES ($1, $2, $3, $4)",
                t1, from_user_id, "u2u", -value
            )
            await conn.execute(
                "INSERT INTO transactions (user_id, transaction_type, value) VALUES ($1, $2, $3, $4)",
                t2, to_user_id, "u2u", value
            )
    finally:
        if conn:
            await conn.close()


async def main():
    from_user_id = "user-1"
    to_user_id = "user-2"
    value = 100
    await wrong_move_tokens(from_user_id, to_user_id, value)
    await one_operation_move_tokens(from_user_id, to_user_id, value)
    await wrong_move_tokens(from_user_id, to_user_id, value)


if __name__ == "__main__":
    asyncio.run(main())
