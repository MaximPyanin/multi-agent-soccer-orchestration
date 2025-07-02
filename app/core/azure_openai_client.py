from langchain_openai import AzureChatOpenAI
from app.services.config_service import AppConfig


class AzureOpenAIClient:
    """
    Client for Azure OpenAI services integration.

    Provides a configured Azure OpenAI client instance for
    language model operations throughout the application.
    """

    def __init__(self, app_config: AppConfig):
        """
        Initialize the Azure OpenAI client.

        Args:
            app_config: Application configuration containing Azure OpenAI settings
        """
        self._llm_instance = AzureChatOpenAI(
            azure_deployment=app_config.AZURE_OPENAI_LLM_DEPLOYMENT,
            azure_endpoint=app_config.AZURE_OPENAI_ENDPOINT,
            api_version=app_config.AZURE_OPENAI_API_VERSION,
            api_key=app_config.AZURE_OPENAI_KEY,
            temperature=app_config.TEMPERATURE,
            top_p=app_config.TOP_P,
            max_tokens=app_config.MAX_NEW_TOKENS,
        )

    @property
    def get_llm_instance(self) -> AzureChatOpenAI:
        """
        Get the configured Azure OpenAI LLM instance.

        Returns:
            Configured AzureChatOpenAI instance
        """
        return self._llm_instance
