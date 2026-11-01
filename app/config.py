from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or a .env file.

    Environment variables (case-insensitive):
        APP_NAME        - display name of the assistant
        API_KEY         - LLM provider API key; when unset the app runs in demo mode
        BASE_URL        - OpenAI-compatible base URL (e.g. https://api.openai.com/v1)
        MODEL_NAME      - vision-capable model name (e.g. gpt-4o-mini)
        REQUEST_TIMEOUT - per-request timeout in seconds
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AgriAI Assistant"
    api_key: str | None = None
    base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4o-mini"
    request_timeout: float = 60.0


settings = Settings()
