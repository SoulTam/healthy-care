from datetime import datetime
import uuid
from sqlalchemy import Boolean, Integer, DateTime, ForeignKey, func, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserDietaryRestriction(Base):
    __tablename__ = "user_dietary_restrictions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )
    allergies: Mapped[list] = mapped_column(JSON, default=list)
    religious: Mapped[list] = mapped_column(JSON, default=list)
    pregnancy: Mapped[bool] = mapped_column(Boolean, default=False)
    pregnancy_trimester: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    other_restrictions: Mapped[list] = mapped_column(JSON, default=list)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
