from app.services.artifact_classifier import ArtifactKind

from .architecture import ARCHITECTURE_TEMPLATE
from .design import DESIGN_TEMPLATE
from .landing_page import LANDING_PAGE_TEMPLATE
from .prd import PRD_TEMPLATE
from .readme import README_TEMPLATE


class TemplateRegistry:

    @staticmethod
    def get(kind: ArtifactKind) -> str:

        mapping = {
            ArtifactKind.README: README_TEMPLATE,
            ArtifactKind.PRD: PRD_TEMPLATE,
            ArtifactKind.ARCHITECTURE: ARCHITECTURE_TEMPLATE,
            ArtifactKind.DESIGN: DESIGN_TEMPLATE,
            ArtifactKind.HTML: LANDING_PAGE_TEMPLATE,
        }

        return mapping.get(kind, "")