from app.schemas.artifact import ArtifactType


def infer_artifact(prompt: str):

    prompt = prompt.lower()

    if "readme" in prompt:
        return "README.md", ArtifactType.MARKDOWN

    if "landing page" in prompt:
        return "landing-page.html", ArtifactType.HTML

    if "html" in prompt:
        return "index.html", ArtifactType.HTML

    if "prd" in prompt:
        return "PRD.md", ArtifactType.MARKDOWN

    if "design" in prompt:
        return "DESIGN.md", ArtifactType.MARKDOWN

    return "artifact.txt", ArtifactType.TEXT