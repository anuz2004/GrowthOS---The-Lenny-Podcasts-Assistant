from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin
from sqlalchemy.orm import relationship

class Workspace(TimestampMixin, Base):
    __tablename__ = "workspaces"
   

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    icon: Mapped[str] = mapped_column(
        String(20),
        default="🚀",
    )

    color: Mapped[str] = mapped_column(
        String(30),
        default="blue",
    )

    default_model: Mapped[str] = mapped_column(
        String(100),
        default="qwen3:8b",
    )

    mode: Mapped[str] = mapped_column(
        String(50),
        default="research",
    )
    chat_sessions = relationship(
        "ChatSession",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )