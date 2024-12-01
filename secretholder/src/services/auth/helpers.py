from typing import TypedDict

from common_utils import DocStringException


class UserInfo(TypedDict):
    user_id: int


class AuthFailed(DocStringException):
    """Неверный логин или пароль =("""


class NoUserForAccessToken(DocStringException):
    """Нет пользователя для этого токена"""
