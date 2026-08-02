from collections.abc import AsyncGenerator

from ollama import AsyncClient, ResponseError

from app.core.exceptions import (
    ModelNotInstalledError,
    OllamaConnectionError,
    ProviderAPIError,
)
from app.core.logger import logger
from app.llm.base import BaseLLM


class OllamaProvider(BaseLLM):

    def __init__(
        self,
        model: str = "qwen3:8b",
    ):
        self.client = AsyncClient(
            host="http://localhost:11434",
        )

        self.model = model

    async def generate(
        self,
        messages: list[dict],
    ) -> str:

        try:

            response = await self.client.chat(
                model=self.model,
                messages=messages,
            )

            return response["message"]["content"]

        except ResponseError as e:

            logger.exception(
                "Ollama generation failed."
            )

            error = str(e).lower()

            if any(
                phrase in error
                for phrase in (
                    "not found",
                    "manifest",
                    "pull",
                    "does not exist",
                )
            ):
                raise ModelNotInstalledError(
                    self.model,
                )

            raise ProviderAPIError(
                provider="Ollama",
                technical=str(e),
            )

        except Exception as e:

            logger.exception(
                "Unexpected Ollama error."
            )

            raise OllamaConnectionError(
                technical=str(e),
            )

    async def stream(
        self,
        messages: list[dict],
    ) -> AsyncGenerator[str, None]:

        try:

            stream = await self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
            )

            async for chunk in stream:

                token = chunk["message"]["content"]

                if token:
                    yield token

        except ResponseError as e:

            logger.exception(
                "Ollama streaming failed."
            )

            error = str(e).lower()

            if any(
                phrase in error
                for phrase in (
                    "not found",
                    "manifest",
                    "pull",
                    "does not exist",
                )
            ):
                raise ModelNotInstalledError(
                    self.model,
                )

            raise ProviderAPIError(
                provider="Ollama",
                technical=str(e),
            )

        except Exception as e:

            logger.exception(
                "Unexpected Ollama streaming error."
            )

            raise OllamaConnectionError(
                technical=str(e),
            )