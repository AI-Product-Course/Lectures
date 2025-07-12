import asyncio
import uuid

import asyncpg
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from pgvector.asyncpg import register_vector


DATABASE_DSN = "postgresql://user:password@localhost:5432/my_db"

CREATE_EXTENSION_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;
"""

CREATE_TABLE_SQL = """
DROP TABLE IF EXISTS items;
CREATE TABLE items (
    id UUID PRIMARY KEY,
    text TEXT NOT NULL,
    embedding vector(768)
);
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);
"""

INSERT_DATA_SQL = """
INSERT INTO items (id, text, embedding) VALUES ($1, $2, $3)
"""

GET_DATA_SQL = """
SELECT * FROM items;
"""

RELEVANT_DOC_TEXT ="Большая языковая модель это языковая модель, состоящая из нейронной сети со множеством параметров (обычно миллиарды весовых коэффициентов и более), обученной на большом количестве неразмеченного текста с использованием обучения без учителя."
IRRELEVANT_DOC_TEXT = "Задачи сокращения размерности. Исходная информация представляется в виде признаковых описаний, причём число признаков может быть достаточно большим. Задача состоит в том, чтобы представить эти данные в пространстве меньшей размерности, по возможности, минимизировав потери информации.."
QUERY_TEXT = "Что такое большая языковая модель?"


embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
relevant_doc_vector, irrelevant_doc_vector = embeddings.embed_documents([RELEVANT_DOC_TEXT, IRRELEVANT_DOC_TEXT])


async def initialize():
    conn: asyncpg.Connection = await asyncpg.connect(DATABASE_DSN)
    try:
        await register_vector(conn)

        await conn.execute(CREATE_EXTENSION_SQL)

        await conn.execute(CREATE_TABLE_SQL)

        await conn.executemany(
            INSERT_DATA_SQL, [
                (uuid.uuid4(), RELEVANT_DOC_TEXT, relevant_doc_vector),
                (uuid.uuid4(), IRRELEVANT_DOC_TEXT, irrelevant_doc_vector),
            ])

        records = await conn.fetch(GET_DATA_SQL)
        print(records)
    finally:
        if conn:
            await conn.close()


if __name__ == "__main__":
    asyncio.run(initialize())
