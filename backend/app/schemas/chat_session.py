from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatSessionCreate(BaseModel):
    workspace_id: int

    title: str = "New Chat"

    provider: str = "ollama"

    model: str = "qwen3:8b"


class ChatSessionResponse(BaseModel):
    id: int
    workspace_id: int

    title: str

    provider: str
    model: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )