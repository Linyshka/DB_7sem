from typing import Annotated

from fastapi import Header, HTTPException, Request, status

from repositories.auth import AuthRepository
from services.auth.auth import AuthService
from services.auth.helpers import NoUserForAccessToken, UserInfo


async def check_access_token(
    request: Request, authorization: Annotated[str | None, Header()] = None
) -> UserInfo:
    try:
        if not authorization or len(authorization.split(" ")) != 2:
            raise NoUserForAccessToken

        async with request.app.state.pg.acquire() as conn:
            repo = AuthRepository(request.app.state.sso_client, conn)
            service = AuthService(repo, None)
            return await service.check_access_token(authorization.split(" ")[-1])
    except (NoUserForAccessToken, IndexError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не предоставлены данные для авторизации(или невалидные)",
        )
