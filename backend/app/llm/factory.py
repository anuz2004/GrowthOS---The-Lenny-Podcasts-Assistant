from xml.parsers.expat import model

from app.llm.providers.ollama_provider import OllamaProvider

# Uncomment when implemented
from app.llm.providers.openai_provider import OpenAIProvider
from app.llm.providers.claude_provider import ClaudeProvider
from app.llm.providers.grok_provider import GrokProvider
from app.llm.providers.groq_provider import GroqProvider


class LLMFactory:

    @staticmethod
    def get_provider(
        provider: str = "ollama",
        model: str = "qwen3:8b",
    ):
        provider = provider.lower()

        if provider == "ollama":
            return OllamaProvider(model=model)

        if provider == "openai":
            return OpenAIProvider(model=model)

        if provider == "anthropic":
            return ClaudeProvider(model=model)
        if provider == "grok":
            return GrokProvider(model=model)
        if provider == "groq":
            return GroqProvider(model=model)

        raise ValueError(
            f"Unknown provider: {provider}"
        )