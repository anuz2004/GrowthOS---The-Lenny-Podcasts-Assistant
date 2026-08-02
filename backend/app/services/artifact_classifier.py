from enum import Enum


class ArtifactKind(str, Enum):
    README = "readme"
    PRD = "prd"
    ARCHITECTURE = "architecture"
    DESIGN = "design"
    HTML = "html"
    MARKDOWN = "markdown"
    REACT = "react"
    CODE = "code"
    OTHER = "other"


class ArtifactClassifier:

    @staticmethod
    def classify(
        prompt: str,
    ) -> ArtifactKind:

        text = prompt.lower()

        if "readme" in text:
            return ArtifactKind.README

        if "prd" in text:
            return ArtifactKind.PRD

        if "architecture" in text:
            return ArtifactKind.ARCHITECTURE

        if "design" in text:
            return ArtifactKind.DESIGN

        if "react" in text:
            return ArtifactKind.REACT

        if "html" in text:
            return ArtifactKind.HTML

        if "markdown" in text:
            return ArtifactKind.MARKDOWN

        if "code" in text:
            return ArtifactKind.CODE

        return ArtifactKind.OTHER