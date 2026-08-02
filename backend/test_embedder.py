import asyncio

from app.rag.embedder import Embedder


async def main():
    embedder = Embedder()

    embedding = await embedder.embed(
        "GrowthOS helps founders build AI-powered products."
    )

    print(f"Embedding dimension: {len(embedding)}")
    print(embedding[:10])


asyncio.run(main())