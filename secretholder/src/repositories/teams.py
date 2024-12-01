from typing import TypedDict

import asyncpg

from common_utils import CantFetchFromStorage


class TeamBasicInfo(TypedDict):
    team_id: int
    team_name: str


class TeamRepository:
    def __init__(self, pg_conn: asyncpg.Connection) -> None:
        self.conn = pg_conn

    async def fetch_teams_by_user_id(self, user_id: int) -> list[TeamBasicInfo]:
        """
        :raises CantFetchFromStorage: if can't insert to db
        """
        try:
            teams = await self.conn.fetch(
                """
                select t.id as team_id, t.name as team_name
                from team_user_permissions tup left join team t on tup.team_id = t.id
                where tup.user_id=$1
                """,
                user_id,
            )
            return [
                {"team_id": team["team_id"], "team_name": team["team_name"]}
                for team in teams
            ]
        except (KeyError, asyncpg.PostgresError) as err:
            print("couldn't fetch teams for user from datebase", err)
            raise CantFetchFromStorage

    async def create_user_personal_secret_space_and_grant_perms(
        self, user_id: int, personal_team_name: str
    ) -> None:
        """
        :raises CantFetchFromStorage: can't insert to db
        """
        try:
            async with self.conn.transaction():
                is_personal = True
                team_id = await self.conn.fetchval(
                    """
                    insert into team (name, owner, is_personal) values($1, $2, $3) returning id
                    """,
                    personal_team_name,
                    user_id,
                    is_personal,
                )
                print("team id exists", team_id)
                # добавили права на персональную группу
                await self.conn.execute(
                    """
                    insert into team_user_permissions (user_id, team_id) values ($1, $2)
                    """,
                    user_id,
                    team_id,
                )

        except asyncpg.PostgresError as err:
            print("not able to create default personal team", err)
            raise CantFetchFromStorage
