from langchain.tools import StructuredTool
from httpx import TimeoutException, HTTPStatusError

from app.services.sports_data_service import SportsDataService
from app.domain.models.team_models import (
    SearchTeamsInput,
    GetTeamDetailsInput,
    FootballTeam,
)


class FootballAPITools:
    """
    Collection of LangChain StructuredTool instances for football data operations.

    Provides two high-level tools:
    - search_teams_by_name: find soccer teams by name or partial name
    - get_team_details_by_id: fetch comprehensive team info by its unique ID

    Both tools delegate actual HTTP interactions and JSON parsing
    to a SportsDataService, and handle transient errors gracefully.
    """

    def __init__(self, sports_data_service: SportsDataService):
        """
        Initialize the FootballAPITools with a SportsDataService.

        Args:
            sports_data_service: Service instance responsible for talking to
                                 TheSportsDB API and returning FootballTeam models.

        Attributes:
            search_teams_by_name (StructuredTool): Tool for searching teams.
            get_team_details_by_id (StructuredTool): Tool for retrieving team details.
        """
        self._sports_data_service = sports_data_service

        self.search_teams_by_name = StructuredTool.from_function(
            name="search_teams_by_name",
            description="Search for soccer teams by name using TheSportsDB API",
            coroutine=self._search_teams_by_name,
            args_schema=SearchTeamsInput,
            return_direct=True,
        )

        self.get_team_details_by_id = StructuredTool.from_function(
            name="get_team_details_by_id",
            description="Get detailed information for a soccer team by ID",
            coroutine=self._get_team_details_by_id,
            args_schema=GetTeamDetailsInput,
            return_direct=True,
        )

    async def _search_teams_by_name(self, team_name: str) -> list[FootballTeam]:
        """
        Internal method: search for football teams matching a name.

        Wrapped by the `search_teams_by_name` StructuredTool.

        Args:
            team_name: Full or partial name of the soccer team to look up.

        Returns:
            A list of FootballTeam objects matching the query.
            Returns an empty list if no teams found or on timeout/HTTP error.
        """
        try:
            return await self._sports_data_service.search_teams_by_name(team_name)
        except (TimeoutException, HTTPStatusError):
            return []

    async def _get_team_details_by_id(self, team_id: str) -> FootballTeam | None:
        """
        Internal method: fetch detailed football team info by its ID.

        Wrapped by the `get_team_details_by_id` StructuredTool.

        Args:
            team_id: Unique identifier for the soccer team in TheSportsDB.

        Returns:
            FootballTeam instance with complete data if found.
            None if the team does not exist or on timeout/HTTP error.
        """
        try:
            return await self._sports_data_service.get_team_details_by_id(team_id)
        except (TimeoutException, HTTPStatusError):
            return None
