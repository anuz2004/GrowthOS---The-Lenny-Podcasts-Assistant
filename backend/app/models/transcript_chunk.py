from datetime import date

from pgvector.sqlalchemy import Vector
from sqlalchemy import Date, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin


class TranscriptChunk(Base, TimestampMixin):
    __tablename__ = "transcript_chunks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    episode: Mapped[str] = mapped_column(
        nullable=False,
        index=True,
    )

    guest: Mapped[str] = mapped_column(
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        nullable=False,
    )

    youtube_url: Mapped[str] = mapped_column(
        nullable=False,
    )

    publish_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(768),
        nullable=False,
    )