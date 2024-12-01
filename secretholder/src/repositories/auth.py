import asyncpg
import httpx
from fastapi import status

from schemas.auth import AuthCreds, SSOResponse, UserToken
from services.auth.helpers import AuthFailed, NoUserForAccessToken, UserInfo
from settings import settings


class AuthRepository:
    def __init__(
        self, sso_client: httpx.AsyncClient, pg_conn: asyncpg.Connection
    ) -> None:
        self.sso_client = sso_client
        self.pg_conn = pg_conn

    async def handle_sso(self, creds: AuthCreds) -> SSOResponse:
        """
        :raises AuthFailed: вернулся не json, неверные креды или пользователя нет впринципе
        """
        try:
            response = await self.sso_client.post(
                settings.sso_handler_url, json=creds.model_dump()
            )
            if response.status_code != status.HTTP_200_OK:
                print("response content", response.content)
                raise AuthFailed

            return response.json()
        except Exception as err:
            print(err)
            raise AuthFailed from None

    async def save_user_and_token(
        self, user_creds: SSOResponse, user_token: str
    ) -> tuple[UserToken, bool]:
        """
        :raises AuthFailed: при ошибках при взаимодействии с бд
        """
        try:
            async with self.pg_conn.transaction():
                user = await self.pg_conn.fetchrow(
                    """
                    select id, token from users where id=$1
                """,
                    user_creds["id"],
                )

                if not user:
                    await self.pg_conn.execute(
                        """
                        insert into users (id, username, token) values ($1, $2, $3)
                    """,
                        user_creds["id"],
                        user_creds["username"],
                        user_token,
                    )
                    print("user inserted")
                    return (
                        UserToken(
                            user_id=user_creds["id"],
                            token=user_token,
                        ),
                        True,
                    )
                return (
                    UserToken(
                        user_id=user["id"],
                        token=user["token"],
                    ),
                    False,
                )
        except asyncpg.PostgresError as err:
            print(err)
            raise AuthFailed from None

    async def get_user_by_token(self, token: str) -> UserInfo:
        """
        :raises NoUserForAccessToken: no user for such token
        """
        try:
            data = await self.pg_conn.fetchrow(
                """
                select id from users where token=$1
            """,
                token,
            )
            return {"user_id": data["id"]}

        except Exception as err:
            print("not able to fetch from database", err)
            raise NoUserForAccessToken from None
