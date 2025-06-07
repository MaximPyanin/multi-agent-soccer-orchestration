from typing import Any

from fastapi import APIRouter
from app.schemas.question_schema import QuestionSchema


class ChatRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/api/v1", tags=["Chat"])
    def get_router(self) -> APIRouter:

        self.router.post("/chat")(self.chat)
        return self.router
    def chat(self, question: QuestionSchema) -> dict[str, dict[str, str]]:
        ...
        return {"data":{"answer":...}}
