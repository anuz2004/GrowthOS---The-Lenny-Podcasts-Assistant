from app.services.agent_router import AgentSkill

from .artifact_skill import ArtifactSkill
from .base import BaseSkill
from .qa_skill import QASkill
from .ship30_skill import Ship30Skill


class SkillRegistry:

    _skills: dict[AgentSkill, BaseSkill] = {
        AgentSkill.QA: QASkill(),
        AgentSkill.SHIP30: Ship30Skill(),
        AgentSkill.ARTIFACT: ArtifactSkill(),
    }

    @classmethod
    def get(cls, skill: AgentSkill) -> BaseSkill:
        return cls._skills[skill]