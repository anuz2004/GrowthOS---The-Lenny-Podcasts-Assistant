from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    chat_session_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    chat_session_id: int
    role: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)