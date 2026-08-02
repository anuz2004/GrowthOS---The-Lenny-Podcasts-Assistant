import asyncio
import traceback
from pathlib import Path

from app.database.session import AsyncSessionLocal
from app.ingest.ingest_service import TranscriptIngestionService
from app.core.config import settings

ROOT = Path(__file__).resolve().parent.parent

EPISODES = (
    ROOT
    / "data"
    / "lennys-podcast-transcripts"
    / "episodes"
)


async def main():

    print("=" * 80)
    print("GrowthOS Knowledge Base Ingestion")
    print("=" * 80)
    print(f"Database : {settings.database_url}")
    print(f"Episodes : {EPISODES}")
    print("=" * 80)

    files = sorted(
        EPISODES.glob("*/transcript.md")
    )

    print(f"Found {len(files)} episodes")
    print()

    service = TranscriptIngestionService()

    async with AsyncSessionLocal() as db:

        for i, file in enumerate(files, start=1):

            print("=" * 80)
            print(f"[{i}/{len(files)}] {file.parent.name}")
            print("=" * 80)

            try:

                await service.ingest(
                    db=db,
                    file_path=file,
                )

            except Exception:

                print("\n❌ INGESTION FAILED\n")

                traceback.print_exc()

                break

    print("\nFinished.")


if __name__ == "__main__":
    asyncio.run(main())