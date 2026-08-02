from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_session import ChatSession
from app.models.message import Message
from app.schemas.message import MessageCreate


class MessageService:

    @staticmethod
    async def create_user_message(
        db: AsyncSession,
        data: MessageCreate,
    ) -> Message:

        session = await db.get(ChatSession, data.chat_session_id)

        if session is None:
            raise ValueError("Chat session not found")

        message = Message(
            chat_session_id=data.chat_session_id,
            role="user",
            content=data.content,
        )

        db.add(message)

        await db.commit()
        await db.refresh(message)

        return message

    @staticmethod
    async def get_session_messages(
        db: AsyncSession,
        session_id: int,
    ) -> list[Message]:

        session = await db.get(ChatSession, session_id)

        if session is None:
            raise ValueError("Chat session not found")

        result = await db.execute(
            select(Message)
            .where(Message.chat_session_id == session_id)
            .order_by(Message.created_at.asc())
        )

        return result.scalars().all()