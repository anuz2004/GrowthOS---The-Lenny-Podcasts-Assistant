from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.ingest.parser import TranscriptParser
from app.models.transcript_chunk import TranscriptChunk
from app.rag.chunker import Chunker
from app.rag.embedder import Embedder


class TranscriptIngestionService:

    def __init__(self):
        self.parser = TranscriptParser()
        self.chunker = Chunker()
        self.embedder = Embedder()

    async def ingest(
        self,
        db: AsyncSession,
        file_path: str | Path,
    ) -> None:

        file_path = Path(file_path)

        # ------------------------------------------
        # Parse Transcript
        # ------------------------------------------

        transcript = self.parser.parse(file_path)

        logger.info(f"Episode : {transcript.title}")
        logger.info(f"Guest   : {transcript.guest}")

        # ------------------------------------------
        # Skip if already indexed
        # ------------------------------------------

        existing = await db.execute(
            select(TranscriptChunk).where(
                TranscriptChunk.episode == transcript.episode
            )
        )

        if existing.scalars().first():

            logger.info("Already indexed.\n")

            return

        # ------------------------------------------
        # Chunk Transcript
        # ------------------------------------------

        chunks = self.chunker.chunk_text(
            transcript.transcript
        )

        logger.info(f"Chunks : {len(chunks)}")

        # ------------------------------------------
        # Generate Embeddings + Insert
        # ------------------------------------------

        try:

            for index, chunk in enumerate(chunks):

                logger.info(
                    f"Embedding {index + 1}/{len(chunks)}"
                )

                embedding = await self.embedder.embed(
                    chunk
                )

                db.add(

                    TranscriptChunk(

                        episode=transcript.episode,

                        guest=transcript.guest,

                        title=transcript.title,

                        youtube_url=transcript.youtube_url,

                        publish_date=transcript.publish_date,

                        chunk_index=index,

                        content=chunk,

                        embedding=embedding,

                    )

                )

            print(">>> ABOUT TO COMMIT")

            await db.commit()

            print(">>> COMMIT SUCCESSFUL")

            logger.info(
                f"Successfully indexed '{transcript.title}'\n"
            )

        except Exception:

            await db.rollback()

            logger.exception(
                f"Failed to ingest {transcript.title}"
            )

            raise