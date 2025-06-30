from typing import Any
from pydantic import BaseModel, Field
from typing import Annotated
from langgraph.graph import add_messages

from app.domain.enums import WorkflowRouteDecision


class ConversationState(BaseModel):
    """
    State model representing the current conversation context.

    Maintains all necessary information throughout the chat workflow
    including user input, routing decisions, and retrieved data.
    """

    user_question: str
    current_route_decision: WorkflowRouteDecision | None = None
    retrieved_context: Annotated[list[dict[str, Any]] | None, add_messages] = Field(
        default_factory=list
    )
    final_answer: str | None = None
