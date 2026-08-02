from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.chat_session import router as chat_session_router
from app.api.v1.message import router as message_router
from app.api.v1.workspace import router as workspace_router

api_router = APIRouter(
    prefix="/api/v1",
)

# Workspace Routes
api_router.include_router(
    workspace_router,
    tags=["Workspaces"],
)

# Chat Session Routes
api_router.include_router(
    chat_session_router,
    tags=["Chat Sessions"],
)

# Message Routes
api_router.include_router(
    message_router,
    tags=["Messages"],
)

# AI Chat Routes
api_router.include_router(
    chat_router,
    tags=["Chat"],
)