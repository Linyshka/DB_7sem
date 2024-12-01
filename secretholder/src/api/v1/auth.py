from fastapi import APIRouter, HTTPException, Request, status

from repositories.auth import AuthRepository
from repositories.teams import TeamRepository
from schemas.auth import AuthCreds
from services.auth.auth import AuthService
from services.auth.helpers import AuthFailed
from services.team.service import TeamService

authorize_router = APIRouter()


@authorize_router.post("/authorize", status_code=status.HTTP_200_OK)
async def authorize(
    creds: AuthCreds,
    request: Request,
):
    async with request.app.state.pg.acquire() as conn:
        auth_repo = AuthRepository(request.app.state.sso_client, conn)
        team_repo = TeamRepository(conn)
        team_service = TeamService(team_repo)
        service = AuthService(auth_repo, team_service)

        try:
            return await service.authenticate_user(creds)
        except AuthFailed as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(err),
            )
