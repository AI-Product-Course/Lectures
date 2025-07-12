import asyncio
from pprint import pprint

import asyncpg
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from pgvector.asyncpg import register_vector


DATABASE_DSN = "postgresql://user:password@localhost:5432/my_db"

GET_NEAREST_DATA_SQL = """
SELECT id, embedding <=> $1 AS distance, text
FROM items
ORDER BY distance
LIMIT $2;
"""


embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
query_vector = embeddings.embed_query("Что такое большая языковая модель?")


async def get_relevant_document():
    conn: asyncpg.Connection = await asyncpg.connect(DATABASE_DSN)
    try:
        await register_vector(conn)

        records = await conn.fetch(GET_NEAREST_DATA_SQL, query_vector, 2)
        pprint(records)
    finally:
        if conn:
            await conn.close()


if __name__ == "__main__":
    asyncio.run(get_relevant_document())