from contextlib import asynccontextmanager

import asyncpg
import httpx
from fastapi import FastAPI

from api import api_router
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pg = await asyncpg.create_pool(
        **settings.dsn_kwargs,
        min_size=10,
        max_size=20,
    )
    client = httpx.AsyncClient(base_url=settings.sso_base_url)
    # чтобы соединение не закрывалось между запросами
    app.state.sso_client = client
    yield
    await client.aclose()
    await app.state.pg.close()


app = FastAPI(lifespan=lifespan)

app.include_router(prefix="/api", router=api_router)
