from enum import Enum


class AgentSkill(str, Enum):
    QA = "qa"
    SHIP30 = "ship30"
    ARTIFACT = "artifact"


class AgentRouter:
    """
    Intent router for GrowthOS.

    Scores each skill based on keyword matches and
    selects the highest scoring skill.
    """

    ARTIFACT_KEYWORDS = {
        "artifact",
        "readme",
        "markdown",
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
        "component",
        "landing",
        "landing page",
        "website",
        "web page",
        "ui",
        "design",
        "generate code",
        "code",
        "template",
        "boilerplate",
        "architecture",
        "architecture document",
        "design document",
        "prd",
        "documentation",
        "technical document",
        "json",
        "sql",
        "yaml",
        "dockerfile",
        "api",
    }

    SHIP30_KEYWORDS = {
        "ship30",
        "essay",
        "article",
        "blog",
        "newsletter",
        "linkedin",
        "thread",
        "twitter",
        "x thread",
        "viral post",
        "write like ship30",
        "long form",
        "story",
        "hook",
    }

    @staticmethod
    def route(message: str) -> AgentSkill:
        text = message.lower().strip()

        artifact_score = sum(
            keyword in text
            for keyword in AgentRouter.ARTIFACT_KEYWORDS
        )

        ship30_score = sum(
            keyword in text
            for keyword in AgentRouter.SHIP30_KEYWORDS
        )

        if artifact_score > ship30_score and artifact_score > 0:
            return AgentSkill.ARTIFACT

        if ship30_score > artifact_score and ship30_score > 0:
            return AgentSkill.SHIP30

        # Tie-breakers
        if artifact_score > 0:
            return AgentSkill.ARTIFACT

        if ship30_score > 0:
            return AgentSkill.SHIP30

        return AgentSkill.QA