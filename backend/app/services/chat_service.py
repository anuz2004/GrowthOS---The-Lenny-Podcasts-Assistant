from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.models.chat_session import ChatSession
from app.models.message import Message
from app.services.agent_router import AgentRouter
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.sse import SSE
from app.skills import SkillRegistry
from app.services.title_service import TitleService
from app.core.exceptions import (
    ChatNotFoundError,
    GrowthOSError,
    ProviderAPIError,
)

class ChatService:
    _rag_service = RAGService()

    @staticmethod
    async def _prepare_chat(
        db: AsyncSession,
        chat_session_id: int,
        content: str,
    ):
        logger.info("=" * 80)
        logger.info("Preparing Chat")
        logger.info("Session ID : %s", chat_session_id)
        logger.info("Prompt     : %s", content[:120])
        logger.info("=" * 80)

        session = await db.get(
            ChatSession,
            chat_session_id,
        )

        if session is None:

            logger.error(
                "Chat session %s not found.",
                chat_session_id,
            )

            raise ChatNotFoundError()

        logger.info(
                "Session Loaded | Provider=%s | Model=%s",
                session.provider,
                session.model,
            )

        skill = AgentRouter.route(content)

        logger.info(
            "Selected Skill : %s",
            skill.value,
        )

        user_message = Message(
            chat_session_id=chat_session_id,
            role="user",
            content=content,
        )

        db.add(user_message)
        await db.flush()

        history = await ConversationService.get_messages(
            db=db,
            chat_session_id=chat_session_id,
        )

        logger.info(
            "Conversation History : %d messages",
            len(history),
        )

        rag = await ChatService._rag_service.retrieve_context(
            db=db,
            query=content,
        )

        logger.info(
            "Retrieved %d transcript chunk(s)",
            len(rag.chunks),
        )

        for chunk in rag.chunks:

            logger.debug(
                "Episode=%s Chunk=%d",
                chunk.episode,
                chunk.chunk_index,
            )

        selected_skill = SkillRegistry.get(skill)

        messages = selected_skill.build_messages(
            prompt=content,
            history=history,
            context=rag.chunks,
        )

        logger.info(
            "Prompt Builder produced %d messages",
            len(messages),
        )

        return (
            session,
            user_message,
            selected_skill,
            messages,
        )

    @staticmethod
    async def send_message(
        db: AsyncSession,
        chat_session_id: int,
        content: str,
    ):

        (
            session,
            user_message,
            selected_skill,
            messages,
        ) = await ChatService._prepare_chat(
            db=db,
            chat_session_id=chat_session_id,
            content=content,
        )

        logger.info("=" * 80)
        logger.info("LLM GENERATION")
        logger.info("Provider : %s", session.provider)
        logger.info("Model    : %s", session.model)
        logger.info("=" * 80)

        try:

            raw_response = await LLMService.generate(
                provider=session.provider,
                model=session.model,
                messages=messages,
            )

        except Exception as e:

            logger.exception(
                "LLM Generation Failed"
            )

            raise ProviderAPIError(
                provider=session.provider,
                technical=str(e),
            )

        logger.info(
            "LLM Response Length : %d chars",
            len(raw_response),
        )

        processed = selected_skill.process_response(
            prompt=content,
            response=raw_response,
        )

        assistant_message = Message(
            chat_session_id=chat_session_id,
            role="assistant",
            content=processed.content,
        )
        # -----------------------------------------------------
# Auto Generate Chat Title
# -----------------------------------------------------

        if session.title == "New Chat":

            try:

                session.title = await TitleService.generate(
                    provider=session.provider,
                    model=session.model,
                    user_prompt=content,
                    assistant_response=processed.content,
                )

                logger.info(
                "Generated chat title: %s",
                session.title,
                )

            except Exception:

                logger.exception(
                    "Failed to generate chat title"
                )

        db.add(assistant_message)

        await db.commit()

        await db.refresh(user_message)
        await db.refresh(assistant_message)
        await db.refresh(session)

        logger.info(
            "Assistant message saved."
        )

        if processed.artifact:
            logger.info(
                "Artifact Generated : %s",
                processed.artifact.type,
            )

        logger.info(
            "Chat Session %s Completed",
            chat_session_id,
        )

        return {
            "user": user_message,
            "assistant": assistant_message,
            "artifact": processed.artifact,
            "title": session.title,
        }

    @staticmethod
    async def stream_message(
        db: AsyncSession,
        chat_session_id: int,
        content: str,
    ) -> AsyncGenerator[str, None]:

        try:

            (
                session,
                user_message,
                selected_skill,
                messages,
            ) = await ChatService._prepare_chat(
                db=db,
                chat_session_id=chat_session_id,
                content=content,
            )

        except Exception as e:

            logger.exception(
                "Failed to prepare chat."
            )

            yield SSE.event(
                "error",
                {
                    "title": "Chat Not Found",
                    "message": str(e),
                    "suggestions": [
                        "Create a new chat.",
                        "Refresh the page.",
                    ],
                },
            )

            yield SSE.event(
                "done",
                {},
            )

            return

        logger.info("=" * 80)
        logger.info("STREAM STARTED")
        logger.info("Provider : %s", session.provider)
        logger.info("Model    : %s", session.model)
        logger.info("=" * 80)

    # ...leave the rest of your existing code unchanged...

        full_response = ""
        token_count = 0

        try:

            async for chunk in LLMService.stream(
                provider=session.provider,
                model=session.model,
                messages=messages,
            ):

                token_count += 1
                full_response += chunk

                yield SSE.event(
                    "token",
                    chunk,
                )

        except Exception as e:

            logger.exception(
                "Streaming Failed"
            )

            yield SSE.event(
                "error",
                {
                    "error": {
                    "title": e.title,
                    "message": e.message,
                    "suggestions": e.suggestions,
                    "technical": e.technical,
                    "status_code": e.status_code,
                }
            },
            )
        except Exception as e:

            logger.exception(
                "Streaming Failed"
            )

            yield SSE.event(
                "error",
                {
                    "error": {
                    "title": "Unexpected Error",
                    "message": "Something unexpected happened while processing your request.",
                    "suggestions": [
                        "Try again.",
                        "Check backend logs.",
                    ],
                    "technical": str(e),
                    "status_code": 500,
                }
            },
        )

            return

        logger.info(
            "Streaming Complete"
        )

        logger.info(
            "Tokens Streamed : %d",
            token_count,
        )

        logger.info(
            "Response Length : %d chars",
            len(full_response),
        )

        processed = selected_skill.process_response(
            prompt=content,
            response=full_response,
        )
        # -----------------------------------------------------
# Auto Generate Chat Title
# -----------------------------------------------------

        if session.title == "New Chat":

            try:

                session.title = await TitleService.generate(
                    provider=session.provider,
                    model=session.model,
                    user_prompt=content,
                    assistant_response=processed.content[:800],
                )

                logger.info(
                    "Generated chat title: %s",
                    session.title,
                )

            except Exception:

                logger.exception(
                    "Failed to generate chat title"
                )

        assistant_message = Message(
            chat_session_id=chat_session_id,
            role="assistant",
            content=processed.content,
        )

        db.add(assistant_message)

        await db.commit()

        await db.refresh(user_message)
        await db.refresh(assistant_message)
        await db.refresh(session)

        logger.info(
            "Assistant message persisted."
        )

        if processed.artifact:

            logger.info(
                "Artifact Generated : %s",
                processed.artifact.type,
            )

            yield SSE.event(
                "artifact",
                processed.artifact.model_dump(),
            )

        yield SSE.event(
            "message",
            {
                "id": assistant_message.id,
                "role": assistant_message.role,
                "content": assistant_message.content,
                "created_at": assistant_message.created_at.isoformat(),
            },
        )
        yield SSE.event(
            "chat_title",
            {
                "id": session.id,
                "title": session.title,
            },
        )

        yield SSE.event(
            "done",
            {},
        )

        logger.info(
            "Streaming Chat %s Completed",
            chat_session_id,
        )

        logger.info("=" * 80)