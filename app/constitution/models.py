from datetime import datetime, date
import uuid
from sqlalchemy import (
    String, Integer, DateTime, Date, ForeignKey,
    Text, func, Numeric,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ConstitutionAssessment(Base):
    __tablename__ = "constitution_assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    constitution_type: Mapped[str] = mapped_column(String(20), nullable=False)
    total_score: Mapped[float] = mapped_column(Numeric(5, 2))
    source: Mapped[str] = mapped_column(
        String(20), default="questionnaire"
    )
    assessment_date: Mapped[date] = mapped_column(Date, nullable=False)
    trend: Mapped[str | None] = mapped_column(String(20), nullable=True)
    summary_report: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    scores: Mapped[list["AssessmentScore"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )


class AssessmentScore(Base):
    __tablename__ = "assessment_scores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("constitution_assessments.id", ondelete="CASCADE"),
        nullable=False,
    )
    dimension: Mapped[str] = mapped_column(String(20), nullable=False)
    score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    assessment: Mapped["ConstitutionAssessment"] = relationship(
        back_populates="scores"
    )
