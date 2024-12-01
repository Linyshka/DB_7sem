from typing import Protocol


class ITeamService(Protocol):
    async def create_default_personal_team_for_user(self, user_id: int):
        """
        :raises CantFetchFromStorage: when storage is not accessible
        """
        ...
