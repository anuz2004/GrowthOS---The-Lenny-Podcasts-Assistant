from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "GrowthOS"

    app_version: str = "1.0.0"

    debug: bool = False

    database_url: str

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    groq_api_key: str | None = None
    xai_api_key: str | None = None

    ollama_host: str = "http://localhost:11434"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()

# --------------------------------------------------
# Startup Diagnostics
# --------------------------------------------------

print("=" * 60)
print("GrowthOS Configuration")
print("=" * 60)

print("OpenAI Key     :", bool(settings.openai_api_key))
print("Anthropic Key  :", bool(settings.anthropic_api_key))
print("Groq Key       :", bool(settings.groq_api_key))
print("xAI Key        :", bool(settings.xai_api_key))
print("Ollama Host    :", settings.ollama_host)

print("=" * 60)