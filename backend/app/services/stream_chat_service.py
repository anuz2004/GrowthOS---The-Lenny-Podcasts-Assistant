from app.llm.factory import LLMFactory


class StreamChatService:

    @staticmethod
    async def stream(
        provider: str,
        model: str,
        messages: list[dict],
    ):

        llm = LLMFactory.get_provider(
            provider=provider,
            model=model,
        )

        async for chunk in llm.stream(messages):

            yield chunk