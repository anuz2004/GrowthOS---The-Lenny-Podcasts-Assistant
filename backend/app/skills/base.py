from abc import ABC, abstractmethod

from app.models.message import Message
from app.models.transcript_chunk import TranscriptChunk
from app.schemas.skill_response import SkillResponse


class BaseSkill(ABC):

    @abstractmethod
    def build_messages(
        self,
        prompt: str,
        history: list[Message],
        context: list[TranscriptChunk] | None,
    ) -> list[dict]:
        """
        Build the messages sent to the LLM.
        """
        ...

    @abstractmethod
    def process_response(
        self,
        prompt: str,
        response: str,
    ) -> SkillResponse:
        """
        Process the raw LLM response.
        """
        ...