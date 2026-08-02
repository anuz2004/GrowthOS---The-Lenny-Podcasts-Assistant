from collections.abc import AsyncGenerator

from app.core.logger import logger
from app.llm.factory import LLMFactory


class LLMService:

    @staticmethod
    async def generate(
        provider: str,
        model: str,
        messages: list[dict],
    ) -> str:

        logger.info(
            "Generating using %s (%s)",
            provider,
            model,
        )

        llm = LLMFactory.get_provider(
            provider,
            model,
        )

        return await llm.generate(
            messages,
        )

    @staticmethod
    async def stream(
        provider: str,
        model: str,
        messages: list[dict],
    ) -> AsyncGenerator[str, None]:

        logger.info(
            "Streaming using %s (%s)",
            provider,
            model,
        )

        llm = LLMFactory.get_provider(
            provider,
            model,
        )

        async for token in llm.stream(
            messages,
        ):
            yield token