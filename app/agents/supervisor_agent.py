from langgraph.types import Command

from app.core.azure_openai_client import AzureOpenAIClient
from app.domain.models.conversation_state import ConversationState
from app.domain.enums import WorkflowRouteDecision


class SupervisorAgent:
    """
    Agent responsible for routing user queries to appropriate processing agents.

    Analyzes user messages and determines the most suitable processing path
    based on content analysis and context requirements.
    """

    def __init__(self, openai_client: AzureOpenAIClient) -> None:
        """
        Initialize the routing supervisor agent.

        Args:
            openai_client: Azure OpenAI client for decision-making
        """
        self._openai_client = openai_client

    async def determine_routing_decision(
        self, conversation_state: ConversationState
    ) -> Command:
        """
        Analyze a user query and determine the appropriate routing decision.

        Args:
            conversation_state: Current conversation state

        Returns:
            Command directing to the appropriate agent(s)
        """
        routing_prompt = (
            "You are the SupervisorAgent. Your ONLY task is to analyze if the user's question is about football/soccer and choose the appropriate routing token.\n\n"
            "FOOTBALL TOPICS include: teams, players, matches, scores, leagues, transfers, statistics, fixtures, results, standings, etc.\n\n"
            "ROUTING RULES:\n"
            "- If question is about football/soccer → output 'search_agent' or 'fotmob_agent' or 'both'\n"
            "- If question is NOT about football/soccer → output 'conversational_agent'\n\n"
            f'User question: "{conversation_state.user_question}"\n\n'
            "Available tokens:\n"
            "conversational_agent — for non-football questions\n"
            "search_agent — for football web search\n"
            "fotmob_agent — for football API data\n"
            "both — for both football sources\n\n"
            "CRITICAL: Output ONLY the token, nothing else:"
        )

        routing_decision = await self._openai_client.get_llm_instance.ainvoke(
            routing_prompt,
        )
        final_decision = routing_decision.content.strip().lower()

        conversation_state.current_route_decision = final_decision

        if final_decision == WorkflowRouteDecision.COMBINED_APPROACH:
            return Command(
                goto=["search_agent", "fotmob_agent"],
                update={"current_route_decision": final_decision},
            )
        else:
            return Command(
                goto=final_decision, update={"current_route_decision": final_decision}
            )
