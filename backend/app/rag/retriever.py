from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.models.transcript_chunk import TranscriptChunk
from app.rag.embedder import Embedder


class Retriever:

    DEFAULT_DISTANCE = 0.45

    STOP_WORDS = {
        "how",
        "what",
        "when",
        "where",
        "why",
        "who",
        "tell",
        "about",
        "does",
        "did",
        "can",
        "could",
        "would",
        "should",
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "into",
        "your",
        "their",
        "have",
        "has",
        "had",
        "was",
        "were",
        "will",
        "also",
    }

    def __init__(self):

        self.embedder = Embedder()

    async def retrieve(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 6,
        max_distance: float = DEFAULT_DISTANCE,
    ):

        logger.info(
            "Retrieving context for query: %s",
            query,
        )

        embedding = await self.embedder.embed_query(
            query
        )

        distance = (
            TranscriptChunk.embedding.cosine_distance(
                embedding
            )
        )

        stmt = (
            select(TranscriptChunk)
            .where(
                distance < max_distance
            )
            .order_by(distance)
            .limit(limit * 4)
        )

        result = await db.execute(stmt)

        chunks = result.scalars().all()

        logger.info(
            "Semantic matches: %d",
            len(chunks),
        )

        if not chunks:
            return []

        query_words = {
            word.lower()
            for word in query.split()
            if (
                len(word) > 2
                and word.lower()
                not in self.STOP_WORDS
            )
        }

        def keyword_score(
            chunk: TranscriptChunk,
        ) -> int:

            score = 0

            title = chunk.title.lower()
            guest = chunk.guest.lower()
            content = chunk.content.lower()

            for word in query_words:

                if word in title:
                    score += 5

                if word in guest:
                    score += 4

                if word in content:
                    score += 1

            return score

        ranked = sorted(
            chunks,
            key=keyword_score,
            reverse=True,
        )

        logger.info(
            "Returning %d chunks",
            min(limit, len(ranked)),
        )

        return ranked[:limit]