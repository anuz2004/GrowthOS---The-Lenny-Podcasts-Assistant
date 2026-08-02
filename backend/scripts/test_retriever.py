import asyncio

from app.database.session import AsyncSessionLocal
from app.rag.retriever import Retriever


QUESTIONS = [
    "How did Airbnb find product market fit?",
    "How should startups hire product managers?",
    "Advice for first time founders",
    "How to build a great product team",
    "Growth loops versus funnels",
]


async def main():

    retriever = Retriever()

    async with AsyncSessionLocal() as db:

        for question in QUESTIONS:

            print("\n")
            print("=" * 100)
            print(question)
            print("=" * 100)

            chunks = await retriever.retrieve(
                db=db,
                query=question,
                limit=5,
            )

            if not chunks:

                print("No matches found.\n")

                continue

            for i, chunk in enumerate(chunks, start=1):

                print(f"\n[{i}]")
                print("-" * 80)
                print(f"Episode : {chunk.title}")
                print(f"Guest   : {chunk.guest}")
                print(f"YouTube : {chunk.youtube_url}")
                print()

                preview = (
                    chunk.content[:400]
                    .replace("\n", " ")
                    .strip()
                )

                print(preview)
                print()


if __name__ == "__main__":
    asyncio.run(main())