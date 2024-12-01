import asyncio

import asyncpg as pg


async def main():
    conn = await pg.connect(
        host="localhost",
        port=5432,
        user="password_manager",
        password="P@ssw0rd",
        database="postgres",
    )
    result = await conn.execute("select 1;")
    print(result)


asyncio.run(main())
