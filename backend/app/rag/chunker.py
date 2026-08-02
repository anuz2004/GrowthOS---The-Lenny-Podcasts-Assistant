from pathlib import Path


class Chunker:

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    # -------------------------------------------------
    # Clean text
    # -------------------------------------------------

    @staticmethod
    def clean(text: str) -> str:

        lines = [
            line.strip()
            for line in text.splitlines()
        ]

        return "\n".join(lines)

    # -------------------------------------------------
    # Chunk Text
    # -------------------------------------------------

    def chunk_text(
        self,
        text: str,
    ) -> list[str]:

        text = self.clean(text)

        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

        chunks = []

        current = ""

        for paragraph in paragraphs:

            # ---------------------------------
            # Huge paragraph
            # ---------------------------------

            if len(paragraph) > self.chunk_size:

                if current:
                    chunks.append(current)
                    current = ""

                start = 0

                while start < len(paragraph):

                    end = start + self.chunk_size

                    chunks.append(
                        paragraph[start:end]
                    )

                    start = (
                        end - self.overlap
                    )

                continue

            # ---------------------------------
            # Normal paragraph
            # ---------------------------------

            if (
                len(current)
                + len(paragraph)
                + 2
                <= self.chunk_size
            ):

                if current:

                    current += (
                        "\n\n"
                        + paragraph
                    )

                else:

                    current = paragraph

            else:

                if current:

                    chunks.append(current)

                    overlap = current[
                        -self.overlap :
                    ]

                    current = (
                        overlap
                        + "\n\n"
                        + paragraph
                    )

                else:

                    current = paragraph

        if current:

            chunks.append(current)

        return chunks

    # -------------------------------------------------
    # Chunk File
    # -------------------------------------------------

    def chunk_file(
        self,
        path: str | Path,
    ) -> list[str]:

        text = Path(path).read_text(
            encoding="utf-8",
        )

        return self.chunk_text(text)