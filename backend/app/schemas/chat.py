from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.artifact import Artifact


class ChatRequest(BaseModel):
    chat_session_id: int
    message: str


class ChatMessage(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatResponse(BaseModel):
    user: ChatMessage
    assistant: ChatMessage
    artifact: Artifact | None = None

    model_config = ConfigDict(from_attributes=True)