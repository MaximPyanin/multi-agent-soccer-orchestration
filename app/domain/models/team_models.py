from pydantic import BaseModel


class FootballTeam(BaseModel):
    """
    Model representing a football team with comprehensive details.

    Contains all relevant information about a football team
    including basic details, location, and social media presence.
    """

    team_id: str
    team_name: str
    alternate_name: str | None = None
    formation_year: str | None = None
    sport_type: str
    league_name: str | None = None
    stadium_name: str | None = None
    stadium_location: str | None = None
    team_description: str | None = None
    badge_image_url: str | None = None
    jersey_image_url: str | None = None
    official_website: str | None = None
    facebook_url: str | None = None
    twitter_url: str | None = None
    youtube_url: str | None = None
