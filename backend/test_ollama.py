import asyncio

from app.llm.providers.ollama_provider import OllamaProvider


async def main():
    llm = OllamaProvider()

    response = await llm.generate(
        "Say hello in one sentence."
    )

    print(response)


asyncio.run(main())