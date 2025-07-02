from pydantic import BaseModel, Field


class UserQuestion(BaseModel):
    """
    Schema for validating user question input.

    Ensures that user questions meet minimum requirements
    before processing in the chat system.
    """

    question: str = Field(min_length=1)
