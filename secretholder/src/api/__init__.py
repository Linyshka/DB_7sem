from fastapi import APIRouter

from .v1 import authorize_router, my_teams_router, team_by_team_id_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(
    prefix="/auth",
    router=authorize_router,
)
api_router.include_router(
    prefix="/teams",
    router=my_teams_router,
)

api_router.include_router(
    prefix="/teams",
    router=team_by_team_id_router,
)
