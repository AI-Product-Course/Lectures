import asyncio
import json
import uuid
from enum import StrEnum

import asyncpg


class TransactionType(StrEnum):
    U2U = "u2u"
    TOP_UP = "top-up"
    LLM = "llm"


DATABASE_DSN = "postgresql://user:password@localhost:5432/my_db"


async def example():
    conn: asyncpg.Connection = await asyncpg.connect(DATABASE_DSN)
    await conn.set_type_codec(
        'jsonb',
        encoder=json.dumps,
        decoder=json.loads,
        schema='pg_catalog'
    )
    await conn.set_type_codec(
        'transaction_type',
        encoder=str,
        decoder=lambda x: TransactionType(x),
        schema='public'
    )
    try:
        transaction_id = uuid.uuid4()
        user_id = uuid.uuid4()
        transaction_type = TransactionType.TOP_UP
        value = 100
        metadata = {"payment-system": "aqua-pay", "promocode": "f21a1f31"}
        tags = ["aqua-pay"]
        await conn.execute(
            "INSERT INTO transactions(id, user_id, transaction_type, value, metadata, tags) VALUES($1, $2, $3, $4, $5, $6);",
            transaction_id, user_id, transaction_type, value, metadata, tags
        )
        records = await conn.fetch("SELECT * FROM transactions;")
        print(records)
    finally:
        if conn:
            await conn.close()


if __name__ == "__main__":
    asyncio.run(example())
