from typing import Any

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from typing import Annotated, List
from operator import add
from app.domain.enums import WorkflowRouteDecision


class ConversationState(BaseModel):
    """
    State model representing the current conversation context.

    Maintains all necessary information throughout the chat workflow,
    including user input, routing decisions, and retrieved data.
    """

    user_question: str
    current_route_decision: WorkflowRouteDecision | None = None
    retrieved_context: Annotated[List[dict[str, Any] | BaseMessage], add] = Field(
        default_factory=list
    )

    final_answer: str | None = None
