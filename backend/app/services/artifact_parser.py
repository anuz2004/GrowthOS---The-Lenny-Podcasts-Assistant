import json
import logging
import re

from app.schemas.artifact import Artifact
from app.schemas.skill_response import SkillResponse

logger = logging.getLogger(__name__)


class ArtifactParser:

    @staticmethod
    def parse(response: str) -> SkillResponse:

        # --------------------------------------------------
        # First try JSON
        # --------------------------------------------------

        try:

            data = json.loads(response)

            artifact = Artifact(
                title=data["title"],
                type=data["type"],
                content=data["content"],
            )

            return SkillResponse(
                content=f"{artifact.title} generated successfully.",
                artifact=artifact,
            )

        except Exception:
            pass

        # --------------------------------------------------
        # Fallback: Markdown code blocks
        # --------------------------------------------------

        match = re.search(
            r"```(\w+)\n([\s\S]*?)```",
            response,
        )

        if match:

            artifact_type = match.group(1).lower()
            artifact_content = match.group(2)

            artifact = Artifact(
                title="Generated Artifact",
                type=artifact_type,
                content=artifact_content,
            )

            logger.info(
                "Detected %s artifact",
                artifact_type,
            )

            return SkillResponse(
                content="Artifact generated successfully.",
                artifact=artifact,
            )

        # --------------------------------------------------
        # Plain text
        # --------------------------------------------------

        return SkillResponse(
            content=response,
            artifact=None,
        )