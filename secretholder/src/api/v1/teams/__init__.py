from .get_team import router as team_by_team_id_router
from .my_teams import router as my_teams_router

__all__ = ("my_teams_router", "team_by_team_id_router")
