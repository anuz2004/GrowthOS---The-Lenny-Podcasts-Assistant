from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.logger import logger
from app.llm.base import BaseLLM


class GroqProvider(BaseLLM):

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
    ):

        logger.info(
            "Initializing Groq Provider (%s)",
            model,
        )

        self.client = AsyncOpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        self.model = model

    async def generate(
        self,
        messages: list[dict],
    ) -> str:

        logger.info(
            "Groq Generate -> %s",
            self.model,
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return (
            response.choices[0]
            .message.content
            or ""
        )

    async def stream(
        self,
        messages: list[dict],
    ) -> AsyncGenerator[str, None]:

        logger.info(
            "Groq Streaming -> %s",
            self.model,
        )

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )

        async for chunk in stream:

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content

            if delta:
                yield delta