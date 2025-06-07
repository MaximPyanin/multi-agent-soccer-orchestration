from pydantic import BaseModel, Field


class QuestionSchema(BaseModel):
    question: str = Field(min_length=1)