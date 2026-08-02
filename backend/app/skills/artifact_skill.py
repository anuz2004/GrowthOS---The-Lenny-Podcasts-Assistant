from app.models.message import Message
from app.models.transcript_chunk import TranscriptChunk
from app.schemas.skill_response import SkillResponse
from app.services.agent_router import AgentSkill
from app.services.artifact_classifier import ArtifactClassifier
from app.services.artifact_parser import ArtifactParser
from app.services.prompt_builder import PromptBuilder
from app.templates import TemplateRegistry

from .base import BaseSkill


class ArtifactSkill(BaseSkill):

    def build_messages(
        self,
        prompt: str,
        history: list[Message],
        context: list[TranscriptChunk] | None,
    ) -> list[dict]:
        enhanced_prompt = self.enhance_prompt(prompt)

        return PromptBuilder.build(
            prompt=enhanced_prompt,
            history=history,
            context=context,
            skill=AgentSkill.ARTIFACT,
        )

    def process_response(
        self,
        prompt: str,
        response: str,
    ) -> SkillResponse:
        """
        Parse the generated artifact returned by the LLM.
        """

        return ArtifactParser.parse(response)

    @staticmethod
    def enhance_prompt(
        prompt: str,
    ) -> str:
        """
        Inject a template based on the requested artifact.
        """

        artifact_kind = ArtifactClassifier.classify(prompt)

        template = TemplateRegistry.get(
            artifact_kind,
        )

        if not template:
            return prompt

        return f"""{template}

User Request:

{prompt}
"""