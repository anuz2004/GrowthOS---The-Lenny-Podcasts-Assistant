from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingest.parser import TranscriptParser
from app.models.transcript_chunk import TranscriptChunk
from app.rag.chunker import Chunker
from app.rag.embedder import Embedder


class TranscriptIngestor:

    def __init__(self):
        self.chunker = Chunker()
        self.embedder = Embedder()

    async def ingest_file(
        self,
        db: AsyncSession,
        file_path: str | Path,
    ):

        transcript = TranscriptParser.parse(file_path)

        print(f"\nEpisode : {transcript.title}")
        print(f"Guest   : {transcript.guest}")

        # ---------------------------------------
        # Skip duplicates
        # ---------------------------------------

        existing = await db.execute(
            select(TranscriptChunk).where(
                TranscriptChunk.episode == transcript.episode
            )
        )

        if existing.scalars().first():

            print("Already ingested.\n")

            return

        # ---------------------------------------
        # Chunk transcript
        # ---------------------------------------

        chunks = self.chunker.chunk_text(
            transcript.transcript
        )

        print(f"Chunks : {len(chunks)}")

        # ---------------------------------------
        # Embed + Save
        # ---------------------------------------

        for index, chunk in enumerate(chunks):

            embedding = await self.embedder.embed(chunk)

            db.add(

                TranscriptChunk(

                    episode=transcript.episode,

                    guest=transcript.guest,

                    title=transcript.title,

                    youtube_url=transcript.youtube_url,

                    publish_date=transcript.publish_date,

                    # source=transcript.source,

                    chunk_index=index,

                    content=chunk,

                    embedding=embedding,
                )

            )

        await db.commit()

        print("✓ Saved\n")