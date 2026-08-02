from app.schemas.artifact import Artifact, ArtifactResponse, ArtifactType


class ArtifactDetector:

    @staticmethod
    def detect(response: str) -> ArtifactResponse:
        response = response.strip()

        if response.startswith("<!DOCTYPE html>") or response.startswith("<html"):
            return ArtifactResponse(
                has_artifact=True,
                artifact=Artifact(
                    title="artifact.html",
                    type=ArtifactType.HTML,
                    content=response,
                ),
            )

        if response.startswith("#"):
            return ArtifactResponse(
                has_artifact=True,
                artifact=Artifact(
                    title="artifact.md",
                    type=ArtifactType.MARKDOWN,
                    content=response,
                ),
            )

        return ArtifactResponse(
            has_artifact=False,
        )