import json

from app.prompts.router_prompt import ROUTER_SYSTEM_PROMPT
from app.schemas.router import RouterResponse


class LLMRouter:

    @staticmethod
    async def classify(
        llm,
        message: str,
    ) -> RouterResponse:

        messages = [
            {
                "role": "system",
                "content": ROUTER_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ]

        response = await llm.generate(messages)

        try:
            data = json.loads(response)
            return RouterResponse(**data)

        except Exception:
            return RouterResponse(skill="qa")