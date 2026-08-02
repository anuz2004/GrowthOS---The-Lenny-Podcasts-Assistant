from collections.abc import AsyncGenerator

from anthropic import AsyncAnthropic

from app.core.config import settings
from app.llm.base import BaseLLM


class ClaudeProvider(BaseLLM):

    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
    ):
        self.client = AsyncAnthropic(
            api_key=settings.anthropic_api_key,
        )

        self.model = model

    @staticmethod
    def _prepare_messages(
        messages: list[dict],
    ) -> tuple[str, list[dict]]:
        """
        Anthropic expects one system prompt and
        conversation messages separately.
        """

        system_parts = []
        conversation = []

        for msg in messages:

            if msg["role"] == "system":
                system_parts.append(
                    msg["content"]
                )

            else:
                conversation.append(
                    {
                        "role": msg["role"],
                        "content": msg["content"],
                    }
                )

        return (
            "\n\n".join(system_parts),
            conversation,
        )

    async def generate(
        self,
        messages: list[dict],
    ) -> str:

        system, conversation = (
            self._prepare_messages(
                messages
            )
        )

        response = await self.client.messages.create(
            model=self.model,
            system=system,
            messages=conversation,
            max_tokens=4096,
        )

        text = ""

        for block in response.content:

            if getattr(block, "type", None) == "text":
                text += block.text

        return text

    async def stream(
        self,
        messages: list[dict],
    ) -> AsyncGenerator[str, None]:

        system, conversation = (
            self._prepare_messages(
                messages
            )
        )

        async with self.client.messages.stream(
            model=self.model,
            system=system,
            messages=conversation,
            max_tokens=4096,
        ) as stream:

            async for text in stream.text_stream:

                if text:
                    yield text