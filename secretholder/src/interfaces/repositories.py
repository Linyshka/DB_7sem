from typing import Protocol

from repositories.teams import TeamBasicInfo
from schemas.auth import AuthCreds, SSOResponse, UserToken
from services.auth.helpers import UserInfo


class IAuthRepository(Protocol):
    async def handle_sso(self, creds: AuthCreds) -> SSOResponse:
        """
        :raises AuthFailed: вернулся не json, неверные креды или пользователя нет впринципе
        """
        ...

    async def save_user_and_token(
        self, user_creds: SSOResponse, user_token: str
    ) -> tuple[UserToken, bool]:
        """
        :raises AuthFailed: при ошибках при взаимодействии с бд
        """

    async def get_user_by_token(self, token: str) -> UserInfo:
        """
        :raises NoUserForAccessToken: no user for such token
        """
        ...


class ITeamRepository(Protocol):
    async def fetch_teams_by_user_id(self, user_id: int) -> list[TeamBasicInfo]:
        """
        :raises CantFetchFromStorage: can't insert to db
        """

    async def create_user_personal_secret_space_and_grant_perms(
        self, user_id: int, personal_team_name: str
    ) -> None:
        """
        :raises CantFetchFromStorage: can't insert to db
        """
