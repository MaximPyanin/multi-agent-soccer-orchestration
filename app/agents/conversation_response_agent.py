from langchain_core.prompts import PromptTemplate
from langgraph.types import Command

from app.core.azure_openai_client import AzureOpenAIClient
from app.domain.models.conversation_state import ConversationState


class ConversationResponseAgent:
    """
    Agent responsible for generating conversational responses based on retrieved information.

    This agent takes user questions and relevant context to provide meaningful answers.
    It handles cases where information is available or unavailable.
    """

    def __init__(self, openai_client: AzureOpenAIClient) -> None:
        """
        Initialize the conversation response agent.

        Args:
            openai_client: Azure OpenAI client for LLM operations
        """
        self._response_template = PromptTemplate(
            input_variables=["user_question", "context_data"],
            template=(
                "You are a conversational agent.\n\n"
                "RULES:\n"
                '- If context_data is None or empty: respond "This question is not relevant to the system."\n'
                "- If context_data is provided: use it to give a concise, helpful answer to the user question.\n\n"
                "User question: {user_question}\n"
                "Context data: {context_data}\n\n"
                "Response:"
            ),
        )

        self._llm = openai_client.get_llm_instance

    async def generate_response(self, conversation_state: ConversationState) -> Command:
        """
        Generate a conversational response based on the current state.

        Args:
            conversation_state: Current conversation state containing question and context

        Returns:
            Command with the generated response
        """
        formatted_prompt = self._response_template.format(
            user_question=conversation_state.user_question,
            context_data=conversation_state.retrieved_context,
        )

        result = await self._llm.ainvoke(formatted_prompt)

        return Command(update={"final_answer": result.content})
