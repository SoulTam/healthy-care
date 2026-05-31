from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.constitution.models import ConstitutionAssessment, AssessmentScore

router = APIRouter(prefix="/api/v1/constitution", tags=["体质趋势"])


@router.get("/history")
async def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    query = (
        select(ConstitutionAssessment)
        .where(ConstitutionAssessment.user_id == user_id)
        .order_by(ConstitutionAssessment.assessment_date.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    assessments = result.scalars().all()

    return {
        "code": "OK",
        "data": [
            {
                "id": str(a.id),
                "constitution_type": a.constitution_type,
                "total_score": float(a.total_score),
                "source": a.source,
                "assessment_date": str(a.assessment_date),
                "trend": a.trend,
            }
            for a in assessments
        ],
        "page": page,
        "page_size": page_size,
    }


@router.get("/history/trend")
async def get_trend(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    result = await db.execute(
        select(ConstitutionAssessment)
        .where(ConstitutionAssessment.user_id == user_id)
        .order_by(ConstitutionAssessment.assessment_date.asc())
    )
    assessments = result.scalars().all()

    data: list[dict] = []
    for a in assessments:
        scores_result = await db.execute(
            select(AssessmentScore).where(
                AssessmentScore.assessment_id == a.id
            )
        )
        scores = {s.dimension: float(s.score) for s in scores_result.scalars().all()}
        data.append({
            "date": str(a.assessment_date),
            "constitution_type": a.constitution_type,
            "total_score": float(a.total_score),
            "scores": scores,
        })

    return {"code": "OK", "data": data}
