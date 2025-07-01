from enum import Enum


class WorkflowRouteDecision(str, Enum):
    """
    Enumeration of possible routing decisions in the workflow.

    Defines the available paths for processing user queries
    based on their content and requirements.
    """

    WEB_SEARCH = "search_agent"
    FOOTBALL_DATA = "fotmob_agent"
    COMBINED_APPROACH = "both"
    DIRECT_CONVERSATION = "conversational_agent"
