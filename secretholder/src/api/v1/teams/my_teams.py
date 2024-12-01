from typing import Annotated

from fastapi import APIRouter, Depends, Request

from dependencies.auth import check_access_token
from repositories.teams import TeamBasicInfo, TeamRepository
from services.auth.helpers import UserInfo

router = APIRouter()


@router.get("/my_teams", response_model=list[TeamBasicInfo])
async def my_teams(
    request: Request,
    user_info: Annotated[UserInfo, Depends(check_access_token)],
):
    async with request.app.state.pg.acquire() as conn:
        team_repo = TeamRepository(conn)
        teams = await team_repo.fetch_teams_by_user_id(user_info["user_id"])
        return teams
