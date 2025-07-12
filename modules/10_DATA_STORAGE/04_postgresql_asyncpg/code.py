import asyncio
import asyncpg


async def main():
    conn: asyncpg.Connection = await asyncpg.connect(host="localhost", port=5432, user="user", password="password", database="my_db")
    try:
        await conn.execute("TRUNCATE TABLE people")
        await conn.execute("CREATE TABLE IF NOT EXISTS people (id SERIAL PRIMARY KEY, name TEXT, age INTEGER)")
        await conn.execute("INSERT INTO people (name, age) VALUES ($1, $2)", 'Иван Иванов', 30)
        records = await conn.fetch("SELECT * FROM people")
        print(records)
        print(records[0]["name"], records[0]["age"])
    finally:
        if conn:
            await conn.close()


asyncio.run(main())