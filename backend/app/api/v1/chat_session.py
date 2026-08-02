from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.models.chat_session import ChatSession
from app.models.workspace import Workspace
from app.schemas.chat_session import (
    ChatSessionCreate,
    ChatSessionResponse,
)

router = APIRouter(
    prefix="/chat-sessions",
    tags=["Chat Sessions"],
)


@router.get(
    "/",
    response_model=list[ChatSessionResponse],
)
async def get_chat_sessions(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatSession)
    )

    return result.scalars().all()


@router.post(
    "/",
    response_model=ChatSessionResponse,
)
async def create_chat_session(
    payload: ChatSessionCreate,
    db: AsyncSession = Depends(get_db),
):
    workspace = await db.get(
        Workspace,
        payload.workspace_id,
    )

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found",
        )

    session = ChatSession(
        workspace_id=payload.workspace_id,
        title=payload.title,
        provider=payload.provider,
        model=payload.model,
    )

    db.add(session)

    await db.commit()
    await db.refresh(session)

    return session


@router.delete(
    "/{chat_session_id}",
)
async def delete_chat_session(
    chat_session_id: int,
    db: AsyncSession = Depends(get_db),
):
    session = await db.get(
        ChatSession,
        chat_session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found",
        )

    await db.delete(session)
    await db.commit()

    return {
        "success": True,
        "message": "Chat session deleted successfully.",
    }