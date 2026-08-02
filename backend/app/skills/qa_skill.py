from app.models.message import Message
from app.models.transcript_chunk import TranscriptChunk
from app.schemas.skill_response import SkillResponse
from app.services.agent_router import AgentSkill
from app.services.prompt_builder import PromptBuilder

from .base import BaseSkill


class QASkill(BaseSkill):

    def build_messages(
        self,
        prompt: str,
        history: list[Message],
        context: list[TranscriptChunk] | None,
    ) -> list[dict]:

        return PromptBuilder.build(
            prompt=prompt,
            history=history,
            context=context,
            skill=AgentSkill.QA,
        )

    def process_response(
        self,
        prompt: str,
        response: str,
    ) -> SkillResponse:

        return SkillResponse(
            content=response,
            artifact=None,
        )