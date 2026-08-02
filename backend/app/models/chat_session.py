from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin


class ChatSession(TimestampMixin, Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        default="New Chat",
    )

    # Which provider powers this chat?
    provider: Mapped[str] = mapped_column(
        String(50),
        default="ollama",
    )

    # Which model inside that provider?
    model: Mapped[str] = mapped_column(
        String(100),
        default="qwen3:8b",
    )

    workspace = relationship(
        "Workspace",
        back_populates="chat_sessions",
    )

    messages = relationship(
        "Message",
        back_populates="chat_session",
        cascade="all, delete-orphan",
    )