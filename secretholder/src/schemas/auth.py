from pydantic import BaseModel


class AuthCreds(BaseModel):
    username: str
    password: str


class SSOResponse(BaseModel):
    id: int
    username: str


class UserToken(BaseModel):
    user_id: int
    token: str
