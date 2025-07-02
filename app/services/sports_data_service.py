from typing import Any
from httpx import AsyncClient, Timeout, TimeoutException, HTTPStatusError

from app.domain.models.team_models import FootballTeam


class SportsDataService:
    """
    Service for interacting with sports data APIs.

    Provides methods to search and retrieve football team information
    from TheSportsDB API with proper error handling and data transformation.
    """

    def __init__(self) -> None:
        """Initialize the sports data service with API configuration."""
        self._api_base_url = "https://www.thesportsdb.com/api/v1/json"
        self._api_key = "3"
        self._http_client = AsyncClient(timeout=Timeout(10.0, connect=5.0))

    @staticmethod
    def _transform_api_data_to_team(raw_data: dict[str, Any]) -> FootballTeam | None:
        """
        Transform raw API data into a FootballTeam model.

        Args:
            raw_data: Raw data dictionary from the API

        Returns:
            FootballTeam instance if data is valid, None otherwise
        """
        if raw_data.get("strSport") != "Soccer":
            return None

        return FootballTeam(
            team_id=raw_data.get("idTeam", ""),
            team_name=raw_data.get("strTeam", ""),
            alternate_name=raw_data.get("strAlternate"),
            formation_year=raw_data.get("intFormedYear"),
            sport_type=raw_data.get("strSport", ""),
            league_name=raw_data.get("strLeague"),
            stadium_name=raw_data.get("strStadium"),
            stadium_location=raw_data.get("strStadiumLocation"),
            team_description=raw_data.get("strDescriptionEN"),
            badge_image_url=raw_data.get("strTeamBadge"),
            jersey_image_url=raw_data.get("strTeamJersey"),
            official_website=raw_data.get("strWebsite"),
            facebook_url=raw_data.get("strFacebook"),
            twitter_url=raw_data.get("strTwitter"),
            youtube_url=raw_data.get("strYoutube"),
        )

    async def _execute_api_request(self, endpoint: str) -> dict[str, Any]:
        """
        Execute HTTP request to the sports API.

        Args:
            endpoint: API endpoint to call

        Returns:
            JSON response data

        Raises:
            HTTPStatusError: If the API request fails
        """
        full_url = f"{self._api_base_url}/{self._api_key}/{endpoint}"
        response = await self._http_client.get(full_url)
        response.raise_for_status()
        return response.json()

    async def search_teams_by_name(self, team_name: str) -> list[FootballTeam]:
        """
        Search for football teams by name.

        Args:
            team_name: Name or partial name of the team to search

        Returns:
            List of matching FootballTeam instances
        """
        try:
            api_response = await self._execute_api_request(
                f"searchteams.php?t={team_name}"
            )
            teams = [
                team.model_dump()
                for raw_team_data in api_response.get("teams", [])
                if (team := self._transform_api_data_to_team(raw_team_data)) is not None
            ]
            return teams
        except (TimeoutException, HTTPStatusError):
            return []

    async def get_team_details_by_id(self, team_id: str) -> FootballTeam | None:
        """
        Get detailed team information by team ID.

        Args:
            team_id: Unique identifier of the team

        Returns:
            FootballTeam instance if found, None otherwise
        """
        try:
            api_response = await self._execute_api_request(
                f"lookupteam.php?id={team_id}"
            )
            raw_team_data = (api_response.get("teams") or [None])[0]
            return (
                self._transform_api_data_to_team(raw_team_data)
                if raw_team_data
                else None
            )
        except (TimeoutException, HTTPStatusError):
            return None
