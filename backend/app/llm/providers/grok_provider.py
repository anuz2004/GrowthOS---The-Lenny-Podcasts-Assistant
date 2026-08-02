from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from app.core.config import settings
from app.llm.base import BaseLLM


class GrokProvider(BaseLLM):

    def __init__(
        self,
        model: str = "grok-4",
    ):
        self.client = AsyncOpenAI(
            api_key=settings.xai_api_key,
            base_url="https://api.x.ai/v1",
        )

        self.model = model

    async def generate(
        self,
        messages: list[dict],
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content or ""

    async def stream(
        self,
        messages: list[dict],
    ) -> AsyncGenerator[str, None]:

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