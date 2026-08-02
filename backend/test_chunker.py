from app.rag.chunker import Chunker

chunker = Chunker(
    chunk_size=100,
    overlap=20,
)

text = (
    "GrowthOS is an AI operating system. " * 30
)

chunks = chunker.chunk_text(text)

print(f"Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}")
    print(chunk)