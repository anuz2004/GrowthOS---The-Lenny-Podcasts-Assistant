from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkspaceCreate(BaseModel):
    title: str
    description: str | None = None


class WorkspaceResponse(BaseModel):
    id: int
    title: str
    description: str | None
    icon: str
    color: str
    default_model: str
    mode: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)