from uuid import uuid4

from interfaces.repositories import IAuthRepository
from interfaces.services import ITeamService
from schemas.auth import AuthCreds, UserToken
from services.auth.helpers import UserInfo


class AuthService:
    def __init__(
        self, auth_repo: IAuthRepository, team_service: ITeamService | None = None
    ) -> None:
        """
        :param team_service: только для метода authenticate_user
        """
        self.repo = auth_repo
        self.team_service = team_service

    async def authenticate_user(self, creds: AuthCreds) -> UserToken:
        """
        :raises AuthFailed: если возникает ошибка, связанная с аутентификацией пользователя
        """
        user_data = await self.repo.handle_sso(creds)
        access_token = str(uuid4())
        user_token, was_created = await self.repo.save_user_and_token(
            user_creds=user_data, user_token=access_token
        )
        if was_created:
            await self.team_service.create_default_personal_team_for_user(
                user_token.user_id
            )
        return user_token

    async def check_access_token(self, token: str) -> UserInfo:
        """
        :raises NoTokenForAccessToken: no token for user
        """
        return await self.repo.get_user_by_token(token)
