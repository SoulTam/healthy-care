from datetime import datetime
import uuid
from sqlalchemy import (
    String, Integer, Text, DateTime, ForeignKey,
    Index, func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source_chapter: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    chunk_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    embedding_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    tags: Mapped[list["ChunkTag"]] = relationship(
        back_populates="chunk", cascade="all, delete-orphan"
    )


class ChunkTag(Base):
    __tablename__ = "chunk_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chunk_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_chunks.id", ondelete="CASCADE"),
        nullable=False,
    )
    dimension: Mapped[str] = mapped_column(String(50), nullable=False)
    tag_value: Mapped[str] = mapped_column(String(100), nullable=False)

    chunk: Mapped["KnowledgeChunk"] = relationship(back_populates="tags")

    __table_args__ = (
        Index("ix_chunk_tags_dimension", "dimension", "tag_value"),
    )
