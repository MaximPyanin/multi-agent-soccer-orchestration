from fastapi import APIRouter

from app.core.graph_builder import GraphBuilder
from app.domain.models.conversation_state import ConversationState
from app.domain.models.user_question import UserQuestion


class ChatRouter:
    """
    API router for chat-related endpoints.

    Handles HTTP requests for chat functionality and coordinates
    with the workflow orchestrator to process user queries.
    """

    def __init__(self, graph_builder: GraphBuilder) -> None:
        """
        Initialize the chat API router.

        Args:
            workflow_orchestrator: Main workflow orchestrator for processing requests
        """
        self._api_router = APIRouter(prefix="/api/v1", tags=["Chat"])
        self._graph_builder = graph_builder

    def get_configured_router(self) -> APIRouter:
        """
        Get the configured API router with registered endpoints.

        Returns:
            Configured FastAPI router
        """
        self._api_router.post("/chat")(self.process_chat_message)
        return self._api_router

    async def process_chat_message(
        self, user_question: UserQuestion
    ) -> dict[str, dict[str, str]]:
        """
        Process incoming chat messages and return responses.

        Args:
            user_question: User's question wrapped in the schema

        Returns:
            Structured response containing the answer
        """
        initial_state = ConversationState(
            user_question=user_question.question,
        )

        final_result = await self._graph_builder.execute_workflow(initial_state)

        return {"data": {"answer": final_result.final_answer}}
