from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    model_name: str = "google/gemma-3-27b-it:free"

    app_env: str = "local"
    log_level: str = "INFO"

    postgres_url: str = ""
    redis_url: str = ""

    database_url: str = "sqlite+aiosqlite:///./incident_platform.db"

    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_base_url: str = "https://cloud.langfuse.com"
    langfuse_tracing_environment: str = "incident-response-dev"

    mcp_server_url: str = ""
    use_real_mcp: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()