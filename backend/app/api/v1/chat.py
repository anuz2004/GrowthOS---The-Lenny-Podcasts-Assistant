from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.database.dependencies import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ChatService.send_message(
            db=db,
            chat_session_id=payload.chat_session_id,
            content=payload.message,
        )

    except ValueError as e:
        logger.warning(str(e))

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception:
        logger.exception(
            "Unexpected error while processing chat request."
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )


@router.post("/stream")
async def stream_chat(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return StreamingResponse(
            ChatService.stream_message(
                db=db,
                chat_session_id=payload.chat_session_id,
                content=payload.message,
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except ValueError as e:
        logger.warning(str(e))

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception:
        logger.exception(
            "Unexpected error while streaming chat."
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )