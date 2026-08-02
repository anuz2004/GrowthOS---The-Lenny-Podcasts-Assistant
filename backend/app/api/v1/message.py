from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post(
    "/",
    response_model=MessageResponse,
)
async def create_message(
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await MessageService.create_user_message(
            db,
            payload,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.get(
    "/{session_id}",
    response_model=List[MessageResponse],
)
async def get_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await MessageService.get_session_messages(
            db,
            session_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )