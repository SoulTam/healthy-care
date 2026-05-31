from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
import uuid


class ChunkTagOut(BaseModel):
    dimension: str
    tag_value: str


class KnowledgeChunkOut(BaseModel):
    id: uuid.UUID
    content: str
    source: str | None = None
    source_chapter: str | None = None
    chunk_index: int | None = None
    status: str = "active"
    created_at: datetime
    tags: list[ChunkTagOut] = []
