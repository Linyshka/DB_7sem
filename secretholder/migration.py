import asyncio
import contextlib
import os

import asyncpg as pg

from settings import settings


def read_query(dir: str, filename: str) -> str:
    """
    return: ddl script
    """
    with open(dir + filename) as file:
        return file.read()


async def main():
    try:
        # create non-default database
        with contextlib.suppress(pg.exceptions.PostgresError):
            conn = await pg.connect(
                **settings.default_dsn_kwargs,
            )
            await conn.execute("CREATE DATABASE pwd_manager;")
            await conn.close()

        new_conn = await pg.connect(**settings.dsn_kwargs)

        # fetch and execute all db migration scripts
        migration_files = os.listdir("migrations")
        ddl_queries = [
            read_query("migrations/", filename) for filename in migration_files
        ]

        for query in ddl_queries:
            print("query", query)
            await new_conn.execute(query)

    except pg.exceptions.PostgresError as err:
        print("Error while migrating database", err)

        exit(-1)


asyncio.run(main())
