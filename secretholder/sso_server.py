from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uvicorn import run

from settings import settings

app = FastAPI()

system_users = [
    {
        "id": 1,
        "username": "admin",
        "password": "temppassword",
    },
    {
        "id": 2,
        "username": "default_user1",
        "password": "temppassword",
    },
    {
        "id": 3,
        "username": "default_user2",
        "password": "temppassword",
    },
]


class Employee(BaseModel):
    username: str
    password: str


@app.post("/sso_authorization")
async def handler(employee: Employee):
    for user in system_users:
        print(user["username"] == employee.username)
        print(user["password"] == employee.password)

        if (
            user["username"] == employee.username
            and user["password"] == employee.password
        ):
            return {"id": user["id"], "username": user["username"]}

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "user not found",
        },
    )


run(
    app,
    host=settings.SSO_SERVER_HOST,
    port=settings.SSO_SERVER_PORT,
)
