from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dependencies.auth import check_access_token
from services.auth.helpers import UserInfo


class SecretDescription(BaseModel):
    id: int
    name: str
    description: str
    str_value: str | None = None
    file_url: str | None = None


class SecretGroupDescription(BaseModel):
    id: int
    name: str
    description: str
    permission_type: Literal["READ", "READWRITE"]
    secrets: list[SecretDescription]


class TeamDescription(BaseModel):
    id: int
    name: str
    secret_groups: list[SecretGroupDescription]


router = APIRouter()


@router.get("/{team_id}", response_model=TeamDescription)
async def get_team_by_team_id(
    request: Request,
    team_id: int,
    user_info: Annotated[UserInfo, Depends(check_access_token)],
):
    async with request.app.state.pg.acquire() as conn:
        query = """
            select 1 from team_user_permissions where team_id=$1 and user_id=$2
        """
        permission_exists = await conn.fetchval(query, team_id, user_info["user_id"])

        if not permission_exists:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": "У пользователя нет доступа к данной команде",
                },
            )

        query = """
            select sg.id as group_id,
                   sg.name as group_name,
                   sg.description as group_descr,
                   sgu.permission_type as permission_type,
                   s.name as secret_name,
                   s.id as secret_id,
                   s.description as secret_descr,
                   s.str_value as secret_str_value,
                   s.file_url as secret_file_url
            from secret_group_user_permissions sgu
            inner join secret_group sg on sg.id = sgu.secret_group_id
            inner join secret s on s.secret_group_id = sg.id
            where sg.team_id = $1 and sgu.user_id = $2
        """

        secret_info = await conn.fetch(query, team_id, user_info["user_id"])
        team_info = await conn.fetch("select * from team where id = $1", team_id)
        if len(team_info) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": f"Нет команды соответствующей {team_id=}",
                },
            )

        group_info = {}
        for item in secret_info:
            current_secret = {
                "id": item["secret_id"],
                "name": item["secret_name"],
                "description": item["secret_descr"],
                "str_value": item["secret_str_value"],
                "file_url": item["secret_file_url"],
            }

            if item["group_id"] not in group_info:
                group_info[item["group_id"]] = {
                    "id": item["group_id"],
                    "name": item["group_name"],
                    "description": item["group_descr"],
                    "secrets": [current_secret],
                    "permission_type": item["permission_type"],
                }
                continue

            group_info[item["group_id"]]["secrets"].append(current_secret)

        response = {
            "id": team_info[0]["id"],
            "name": team_info[0]["name"],
            "is_personal": team_info[0]["is_personal"],
            "secret_groups": list(group_info.values()),
        }

        return response
