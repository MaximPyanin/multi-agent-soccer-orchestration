import os

from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.chat_router import ChatRouter
from app.agents.supervisor_agent import SupervisorAgent
from app.agents.football_data_agent import FootballDataAgent
from app.agents.web_search_agent import WebSearchAgent
from app.agents.conversation_response_agent import ConversationResponseAgent
from app.controllers.agents_controller import AgentsController
from app.core.graph_builder import GraphBuilder
from app.core.azure_openai_client import AzureOpenAIClient
from app.services.config_service import AppConfig
from app.services.sports_data_service import SportsDataService
from app.tools.football_api_tools import FootballAPITools


load_dotenv()


def main():
    config = AppConfig(os.environ)
    sports_data_service = SportsDataService()
    football_api_tools = FootballAPITools(sports_data_service)
    azure_openai_client = AzureOpenAIClient(config)
    football_data_agent = FootballDataAgent(azure_openai_client, football_api_tools)
    web_search_agent = WebSearchAgent()
    conversation_response_agent = ConversationResponseAgent(azure_openai_client)
    supervisor_agent = SupervisorAgent(azure_openai_client)
    agents_controller = AgentsController(
        supervisor_agent,
        football_data_agent,
        web_search_agent,
        conversation_response_agent,
    )
    graph_builder = GraphBuilder(agents_controller)
    chat_router = ChatRouter(graph_builder)

    app = FastAPI()
    app.include_router(chat_router.get_configured_router())
    return app


app = main()
