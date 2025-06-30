from langgraph.types import Command

from app.domain.models.conversation_state import ConversationState
from app.agents.football_data_agent import FootballDataAgent
from app.agents.web_search_agent import WebSearchAgent
from app.agents.conversation_response_agent import ConversationResponseAgent
from app.agents.supervisor_agent import SupervisorAgent


class AgentsController:
    """
    Controller for coordinating execution of different agents in the chat workflow.

    Manages the interaction between agents and ensures the proper flow of information
    through the chat processing pipeline with centralized execution control.
    """

    def __init__(
        self,
        supervisor_agent: SupervisorAgent,
        football_agent: FootballDataAgent,
        web_search_agent: WebSearchAgent,
        conversation_agent: ConversationResponseAgent,
    ) -> None:
        """
        Initialize the agent execution controller.

        Args:
            supervisor_agent: Agent for routing decisions
            football_agent: Agent for football data operations
            web_search_agent: Agent for web search operations
            conversation_agent: Agent for generating responses
        """
        self._supervisor_agent = supervisor_agent
        self._football_data_agent = football_agent
        self._web_search_agent = web_search_agent
        self._conversation_response_agent = conversation_agent

    async def get_routing_decision(
        self, conversation_state: ConversationState
    ) -> Command:
        """
        Route request to the appropriate agent.

        Args:
            conversation_state: Current state of the conversation

        Returns:
            Command directing to the appropriate next agent
        """
        return await self._supervisor_agent.determine_routing_decision(
            conversation_state
        )

    async def search_web(self, conversation_state: ConversationState) -> Command:
        """
        Execute web search processing.

        Args:
            conversation_state: Current state of the conversation

        Returns:
            Command with search results
        """
        return await self._web_search_agent.search_web_content(conversation_state)

    async def fetch_football_data(
        self, conversation_state: ConversationState
    ) -> Command:
        """
        Execute football data retrieval.

        Args:
            conversation_state: Current state of the conversation

        Returns:
            Command with football data results
        """
        return await self._football_data_agent.process_football_query(
            conversation_state
        )

    async def generate_response(self, conversation_state: ConversationState) -> Command:
        """
        Generate conversation response.

        Args:
            conversation_state: Current state of the conversation

        Returns:
            Command with the final response
        """
        return await self._conversation_response_agent.generate_response(
            conversation_state
        )
