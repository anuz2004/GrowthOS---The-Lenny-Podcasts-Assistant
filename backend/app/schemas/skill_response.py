from pydantic import BaseModel

from app.schemas.artifact import Artifact


class SkillResponse(BaseModel):
    content: str
    artifact: Artifact | None = None