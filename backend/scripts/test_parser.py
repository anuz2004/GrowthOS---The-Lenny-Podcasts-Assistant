from pathlib import Path

from app.ingest.parser import TranscriptParser

repo = Path(
    "data/lennys-podcast-transcripts/episodes"
)

first = next(
    repo.glob("*/transcript.md")
)

transcript = TranscriptParser.parse(first)

print(transcript)