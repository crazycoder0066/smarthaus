"""Application settings, loaded from the environment / a local .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- service ---
    app_name: str = "SmartHaus"
    environment: str = "development"
    log_level: str = "INFO"
    json_logs: bool = False  # set True in prod for machine-readable logs

    # --- LLM (Ollama by default; swap to Bedrock later) ---
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama3.1"
    temperature: float = 0.0

    # request budget for a single agent turn
    agent_timeout_seconds: float = 60.0


@lru_cache
def get_settings() -> Settings:
    """Cached accessor so settings are parsed from the env only once."""
    return Settings()
