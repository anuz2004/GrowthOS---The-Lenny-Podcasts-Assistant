import asyncio

from app.database.session import AsyncSessionLocal
from app.rag.retriever import Retriever


async def main():

    async with AsyncSessionLocal() as db:

        retriever = Retriever()

        results = await retriever.retrieve(
            db,
            "How should founders grow their startup?"
        )

        for chunk in results:
            print("=" * 80)
            print(f"Source : {chunk.source}")
            print(f"Chunk  : {chunk.chunk_index}")
            print(chunk.content)


asyncio.run(main())