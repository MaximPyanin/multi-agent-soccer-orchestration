from langchain.tools import tool
from httpx import TimeoutException, HTTPStatusError

from app.services.sports_data_service import SportsDataService
from app.domain.models.team_models import FootballTeam


class FootballAPITools:
    """
    Collection of tools for football data operations.

    Provides LangChain-compatible tools for searching and retrieving
    football team information from external APIs.
    """

    def __init__(self, sports_data_service: SportsDataService):
        """
        Initialize football API tools.

        Args:
            sports_data_service: Service for sports data operations
        """
        self._sports_data_service = sports_data_service

    @tool(
        "search_teams_by_name",
        description="Search for Soccer teams by name using TheSportsDB API and return a list of Team objects.",
        return_direct=True,
        parse_docstring=True,
    )
    async def search_teams_by_name(self, team_name: str) -> list[FootballTeam]:
        """
        Search for Soccer teams by their name.

        Args:
            team_name: The name (or partial name) of the team to search for.

        Returns:
            A list of FootballTeam instances matching the search query. Empty list if none found or on error.
        """
        try:
            return await self._sports_data_service.search_teams_by_name(team_name)
        except (TimeoutException, HTTPStatusError):
            return []

    @tool(
        "get_team_details_by_id",
        description="Retrieve detailed information for a Soccer team by its ID using TheSportsDB API and return a Team object or None.",
        return_direct=True,
        parse_docstring=True,
    )
    async def get_team_details_by_id(self, team_id: str) -> FootballTeam | None:
        """
        Get detailed information for a Soccer team by its unique ID.

        Args:
            team_id: The unique identifier of the team.

        Returns:
            A FootballTeam instance if found, otherwise None (including on timeout or HTTP error).
        """
        try:
            return await self._sports_data_service.get_team_details_by_id(team_id)
        except (TimeoutException, HTTPStatusError):
            return None
