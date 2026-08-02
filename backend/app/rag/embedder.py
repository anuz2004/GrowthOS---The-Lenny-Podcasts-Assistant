from openai import AsyncOpenAI

from app.core.config import settings
from app.core.logger import logger


class Embedder:

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

        self.model = "text-embedding-3-small"

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

            response = await self.client.embeddings.create(
                model=self.model,
                input=text,
            )

            embedding = response.data[0].embedding

            logger.debug(
                "Embedding dimension: %d",
                len(embedding),
            )

            return embedding

        except Exception as e:

            logger.exception(
                "OpenAI embedding request failed."
            )

            raise RuntimeError(
                f"Failed to generate embeddings using OpenAI: {e}"
            )

    async def embed_query(
        self,
        query: str,
    ) -> list[float]:

        logger.debug(
            "Embedding query: %s",
            query,
        )

        return await self.embed(query)