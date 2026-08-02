from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class ConversationService:

    @staticmethod
    async def get_messages(
        db: AsyncSession,
        chat_session_id: int,
    ) -> list[Message]:

        result = await db.execute(
            select(Message)
            .where(Message.chat_session_id == chat_session_id)
            .order_by(Message.created_at.asc())
        )

        return result.scalars().all()