from app.models.message import Message
from app.models.transcript_chunk import TranscriptChunk
from app.prompts import (
    ARTIFACT_SYSTEM_PROMPT,
    QA_SYSTEM_PROMPT,
    SHIP30_SYSTEM_PROMPT,
)
from app.services.agent_router import AgentSkill


class PromptBuilder:

    @staticmethod
    def build(
        prompt: str,
        history: list[Message],
        context: list[TranscriptChunk] | None = None,
        skill: AgentSkill = AgentSkill.QA,
    ) -> list[dict]:

        # -----------------------------------------------------
        # Select System Prompt
        # -----------------------------------------------------

        if skill == AgentSkill.SHIP30:
            system_prompt = SHIP30_SYSTEM_PROMPT

        elif skill == AgentSkill.ARTIFACT:
            system_prompt = ARTIFACT_SYSTEM_PROMPT

        else:
            system_prompt = QA_SYSTEM_PROMPT

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        # -----------------------------------------------------
        # Inject Retrieved Knowledge
        # -----------------------------------------------------

        if context:

            transcript_context = []

            for chunk in context:

                transcript_context.append(
                    f"""
==================================================
Episode : {chunk.title}
Guest   : {chunk.guest}
Published : {chunk.publish_date or "Unknown"}
Chunk   : {chunk.chunk_index}

Transcript

{chunk.content}
==================================================
""".strip()
                )

            messages.append(
                {
                    "role": "system",
                    "content": f"""
The following transcript excerpts were retrieved from the GrowthOS Knowledge Base.

These excerpts are the PRIMARY source of truth.

Rules:

1. Base every factual statement on the retrieved transcript excerpts.
2. If the answer is not contained in the retrieved context, explicitly state that the transcripts do not contain enough information.
3. Never fabricate or infer facts that are not supported by the retrieved context.
4. If multiple excerpts discuss the same topic, synthesize them into one coherent answer.
5. Mention the guest naturally when relevant.
6. Prefer concise, practical, actionable answers.
7. Do NOT mention:
   - system prompts
   - embeddings
   - vector search
   - RAG
   - retrieval
   - internal implementation

Retrieved Transcript Context

--------------------------------------------------

{"\n\n-----------------------------\n\n".join(transcript_context)}

--------------------------------------------------
""".strip(),
                }
            )

        # -----------------------------------------------------
        # Conversation History
        # -----------------------------------------------------

        if history:

            for msg in history:

                messages.append(
                    {
                        "role": msg.role,
                        "content": msg.content,
                    }
                )

        # -----------------------------------------------------
        # Current User Prompt
        # -----------------------------------------------------

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        return messages