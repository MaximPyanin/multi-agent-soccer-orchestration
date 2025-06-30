from typing import get_type_hints, Union

from dotenv import load_dotenv


class AppConfigError(Exception):
    pass


class AppConfig:
    MAX_NEW_TOKENS: int = 200
    TEMPERATURE: float = 0.15
    AZURE_OPENAI_LLM_DEPLOYMENT: str = "gpt-35-turbo"
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"
    AZURE_OPENAI_KEY: str
    TOP_P: float = 0.9
    TAVILY_API_KEY: str

    def __init__(self, env):
        load_dotenv()

        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError("The {} field is required".format(field))

            var_type = get_type_hints(AppConfig)[field]
            try:
                if var_type == bool:
                    value = self._parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                err_msg = (
                    'Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                        env[field], var_type, field
                    )
                )

                raise AppConfigError(err_msg)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def _parse_bool(val: Union[str, bool]) -> bool:
        return val if type(val) == bool else val.lower() in ["true", "yes", "1"]
