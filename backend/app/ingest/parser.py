from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml


@dataclass
class Transcript:

    episode: str

    guest: str

    title: str

    youtube_url: str

    publish_date: date | None

    transcript: str

    # source: str


class TranscriptParser:

    @staticmethod
    def parse(path: str | Path) -> Transcript:

        path = Path(path)

        text = path.read_text(
            encoding="utf-8",
        )

        # -----------------------------
        # Split YAML
        # -----------------------------

        if not text.startswith("---"):
            raise ValueError(
                f"{path} has no YAML header."
            )

        _, yaml_text, markdown = text.split(
            "---",
            2,
        )

        metadata = yaml.safe_load(
            yaml_text,
        )

        publish_date = None

        if metadata.get("publish_date"):

            try:

                publish_date = date.fromisoformat(
                    metadata["publish_date"]
                )

            except Exception:

                pass

        return Transcript(

            episode=path.parent.name,

            guest=metadata.get(
                "guest",
                "",
            ),

            title=metadata.get(
                "title",
                "",
            ),

            youtube_url=metadata.get(
                "youtube_url",
                "",
            ),

            publish_date=publish_date,

            transcript=markdown.strip(),

            # source=str(path),
        )