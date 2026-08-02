import asyncio

from app.database.session import AsyncSessionLocal
from backend.app.ingest.ingest import TranscriptIngestor


async def main():

    async with AsyncSessionLocal() as db:

        ingestor = TranscriptIngestor()

        await ingestor.ingest_file(
            db=db,
            file_path="transcript_data/raw/sample.txt",
        )


asyncio.run(main())