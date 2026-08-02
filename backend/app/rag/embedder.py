from ollama import AsyncClient, ResponseError

from app.core.config import settings
from app.core.exceptions import (
    ModelNotInstalledError,
    OllamaConnectionError,
)
from app.core.logger import logger


class Embedder:

    def __init__(self):

        self.client = AsyncClient(
            host=settings.ollama_host,
        )

        self.model = "nomic-embed-text"

        logger.info(
            "Embedder initialized (%s)",
            self.model,
        )

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        logger.debug(
            "Embedding %d characters",
            len(text),
        )

        try:

            response = await self.client.embeddings(
                model=self.model,
                prompt=text,
            )

        except ResponseError as e:

            logger.exception(
                "Embedding request failed."
            )

            error = str(e).lower()

            if (
                "not found" in error
                or "model" in error
                and "not exist" in error
            ):
                raise ModelNotInstalledError(
                    self.model,
                )

            raise OllamaConnectionError(
                technical=str(e),
            )

        except Exception as e:

            logger.exception(
                "Unexpected embedding failure."
            )

            raise OllamaConnectionError(
                technical=str(e),
            )

        embedding = response["embedding"]

        logger.debug(
            "Embedding dimension: %d",
            len(embedding),
        )

        return embedding

    async def embed_query(
        self,
        query: str,
    ) -> list[float]:

        logger.debug(
            "Embedding query: %s",
            query,
        )

        return await self.embed(query)