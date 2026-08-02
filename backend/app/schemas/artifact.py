from enum import Enum

from pydantic import BaseModel


class ArtifactType(str, Enum):
    MARKDOWN = "markdown"
    HTML = "html"
    TEXT = "text"


class Artifact(BaseModel):
    title: str
    type: ArtifactType
    content: str


class ArtifactResponse(BaseModel):
    has_artifact: bool
    artifact: Artifact | None = None