from app.services.llm_service import LLMService


class TitleService:

    @staticmethod
    async def generate(
        provider: str,
        model: str,
        user_prompt: str,
        assistant_response: str,
    ) -> str:

        messages = [
            {
                "role": "system",
                "content": """
Generate a concise title for this conversation.

Rules:
- Maximum 6 words.
- No quotation marks.
- No markdown.
- No punctuation unless necessary.
- Return ONLY the title.
""",
            },
            {
                "role": "user",
                "content": f"""
User:
{user_prompt}

Assistant:
{assistant_response}
""",
            },
        ]

        title = await LLMService.generate(
            provider=provider,
            model=model,
            messages=messages,
        )

        # -----------------------------------------------------
        # Clean the generated title
        # -----------------------------------------------------

        title = (
            title.strip()
            .replace('"', "")
            .replace("'", "")
        )

        if title.lower().startswith("title:"):
            title = title[6:].strip()

        title = title.rstrip(".:,- ")

        if not title:
            return "New Chat"

        return title[:255]