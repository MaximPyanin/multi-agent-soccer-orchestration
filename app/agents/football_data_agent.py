import json
import uuid

from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage
from langgraph.types import Command

from app.core.azure_openai_client import AzureOpenAIClient
from app.domain.models.conversation_state import ConversationState
from app.tools.football_api_tools import FootballAPITools


class FootballDataAgent:
    """
    Specialized agent for handling football team data queries.

    Uses football-specific tools to search and retrieve team information
    from external APIs without generating synthetic data.
    """

    def __init__(
        self, openai_client: AzureOpenAIClient, football_tools: FootballAPITools
    ) -> None:
        """
        Initialize the football data agent.

        Args:
            openai_client: Azure OpenAI client for LLM operations
            football_tools: Tools for football data operations
        """
        system_prompt = SystemMessage(
            content=(
                "You are FootballDataAgent. Your ONLY job is to call exactly one tool "
                "and return its raw JSON. You MUST NOT hallucinate or add commentary.\n\n"
                "Tools:\n"
                "  1) search_teams_by_name(team_name: str)\n"
                "  2) get_team_details_by_id(team_id: str)\n"
            )
        )

        self._agent = initialize_agent(
            tools=[
                football_tools.search_teams_by_name,
                football_tools.get_team_details_by_id,
            ],
            llm=openai_client.get_llm_instance,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            system_messages=[system_prompt],
        )

    async def process_football_query(
        self, conversation_state: ConversationState
    ) -> Command:
        """
        Process football-related queries using available tools.

        Args:
            conversation_state: Current conversation state

        Returns:
            Command directing to the next step with retrieved data
        """
        result = await self._agent.ainvoke(conversation_state.user_question)

        msg = {
            "role": "tool",
            "content": json.dumps(result, ensure_ascii=False),
            "tool_call_id": str(uuid.uuid4()),
        }
        return Command(
            goto="conversational_agent",
            update={"retrieved_context": [msg]},
        )
