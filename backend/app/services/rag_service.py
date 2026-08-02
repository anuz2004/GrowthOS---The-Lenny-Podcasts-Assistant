from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transcript_chunk import TranscriptChunk
from app.rag.retriever import Retriever


@dataclass
class Citation:

    episode: str

    guest: str

    youtube_url: str


@dataclass
class RAGResult:

    context: str

    citations: list[Citation]

    chunks: list[TranscriptChunk]


class RAGService:

    def __init__(self):

        self.retriever = Retriever()

    async def retrieve_context(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 6,
    ) -> RAGResult:

        chunks = await self.retriever.retrieve(
            db=db,
            query=query,
            limit=limit,
        )

        if not chunks:

            return RAGResult(
                context="",
                citations=[],
                chunks=[],
            )

        context_parts = []

        citations = []

        for chunk in chunks:

            context_parts.append(
                f"""
Episode: {chunk.title}
Guest: {chunk.guest}

{chunk.content}
"""
            )

            citations.append(
                Citation(
                    episode=chunk.title,
                    guest=chunk.guest,
                    youtube_url=chunk.youtube_url,
                )
            )

        return RAGResult(
            context="\n\n----------------------\n\n".join(
                context_parts
            ),
            citations=citations,
            chunks=chunks,
        )