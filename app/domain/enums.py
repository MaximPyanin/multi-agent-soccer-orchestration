from enum import Enum


class WorkflowRouteDecision(str, Enum):
    """
    Enumeration of possible routing decisions in the workflow.

    Defines the available paths for processing user queries
    based on their content and requirements.
    """

    WEB_SEARCH = "search"
    FOOTBALL_DATA = "stats"
    COMBINED_APPROACH = "both"
    DIRECT_CONVERSATION = "conversation"
