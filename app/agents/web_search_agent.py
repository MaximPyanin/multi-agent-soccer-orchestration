import json
import uuid

from langchain_tavily import TavilySearch
from langgraph.types import Command

from app.domain.models.conversation_state import ConversationState


class WebSearchAgent:
    """
    Agent for performing web searches on football-related topics.

    Provides direct access to web search capabilities without LLM processing,
    focusing on retrieving relevant information from the internet.
    """

    def __init__(self) -> None:
        """Initialize the web search agent with general search capability."""
        self._search_tool = TavilySearch(topic="general")

    async def search_web_content(
        self, conversation_state: ConversationState
    ) -> Command:
        """
        Perform web search based on a user query.

        Args:
            conversation_state: Current conversation state containing the search query

        Returns:
            Command directing to conversation agent with search results
        """
        football_query = f"football soccer {conversation_state.user_question}"
        raw_results = await self._search_tool.ainvoke(football_query)

        msg = {
            "role": "tool",
            "content": json.dumps(raw_results, ensure_ascii=False),
            "tool_call_id": str(uuid.uuid4()),
        }

        return Command(goto="conversational_agent", update={"retrieved_context": [msg]})
