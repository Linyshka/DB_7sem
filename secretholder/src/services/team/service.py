from interfaces.repositories import ITeamRepository


class TeamService:
    DEFAULT_PERSONAL_TEAM_NAME = "Personal SecretSpace"

    def __init__(self, repo: ITeamRepository):
        self.repo = repo

    async def create_default_personal_team_for_user(self, user_id: int):
        """
        :raises CantFetchFromStorage: when storage is not accessible
        """
        await self.repo.create_user_personal_secret_space_and_grant_perms(
            user_id, self.DEFAULT_PERSONAL_TEAM_NAME
        )
