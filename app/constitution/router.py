from __future__ import annotations

from datetime import date, timedelta
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.constitution.models import ConstitutionAssessment, AssessmentScore
from app.constitution.algorithm import (
    QUESTIONS, calculate_scores, determine_constitution,
)
from app.constitution.report_generator import generate_report

router = APIRouter(prefix="/api/v1/constitution", tags=["体质评估"])


class AssessRequest(BaseModel):
    answers: dict[int, int]


@router.get("/questions")
async def get_questions():
    return {
        "code": "OK",
        "data": [
            {
                "id": q["id"],
                "question": q["question"],
                "options": q["options"],
            }
            for q in QUESTIONS
        ],
    }


@router.post("/assess")
async def assess(
    req: AssessRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])

    latest_result = await db.execute(
        select(ConstitutionAssessment)
        .where(ConstitutionAssessment.user_id == user_id)
        .order_by(ConstitutionAssessment.assessment_date.desc())
        .limit(1)
    )
    latest = latest_result.scalar_one_or_none()
    if latest:
        days_since = (date.today() - latest.assessment_date).days
        if days_since < 7:
            raise HTTPException(
                status_code=400,
                detail=f"两次评估间隔需至少 7 天（距上次评估仅 {days_since} 天）",
            )

    scores = calculate_scores(req.answers)
    constitution_type = determine_constitution(scores)

    if latest:
        if scores.get(constitution_type, 0) < (
            latest.total_score or 0
        ):
            trend = "declining"
        elif scores.get(constitution_type, 0) > (
            latest.total_score or 0
        ):
            trend = "improving"
        else:
            trend = "stable"
    else:
        trend = None

    report_text = generate_report(constitution_type, scores, trend)

    assessment = ConstitutionAssessment(
        user_id=user_id,
        constitution_type=constitution_type,
        total_score=scores.get(constitution_type, 0),
        source="questionnaire",
        assessment_date=date.today(),
        trend=trend,
        summary_report=report_text,
    )
    db.add(assessment)
    await db.flush()

    for dim, score in scores.items():
        db.add(AssessmentScore(
            assessment_id=assessment.id,
            dimension=dim,
            score=score,
        ))

    return {
        "code": "OK",
        "data": {
            "id": str(assessment.id),
            "constitution_type": constitution_type,
            "total_score": float(assessment.total_score),
            "scores": scores,
            "trend": trend,
        },
    }


@router.get("/result/{assessment_id}")
async def get_result(
    assessment_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(ConstitutionAssessment).where(
            ConstitutionAssessment.id == uuid.UUID(assessment_id)
        )
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="评估记录不存在")

    scores_result = await db.execute(
        select(AssessmentScore).where(
            AssessmentScore.assessment_id == assessment.id
        )
    )
    scores_list = scores_result.scalars().all()

    return {
        "code": "OK",
        "data": {
            "id": str(assessment.id),
            "constitution_type": assessment.constitution_type,
            "total_score": float(assessment.total_score),
            "source": assessment.source,
            "assessment_date": str(assessment.assessment_date),
            "trend": assessment.trend,
            "scores": {s.dimension: float(s.score) for s in scores_list},
            "report": assessment.summary_report,
        },
    }


@router.get("/latest")
async def get_latest(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    result = await db.execute(
        select(ConstitutionAssessment)
        .where(ConstitutionAssessment.user_id == user_id)
        .order_by(ConstitutionAssessment.assessment_date.desc())
        .limit(1)
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        return {"code": "OK", "data": None}

    scores_result = await db.execute(
        select(AssessmentScore).where(
            AssessmentScore.assessment_id == assessment.id
        )
    )

    return {
        "code": "OK",
        "data": {
            "id": str(assessment.id),
            "constitution_type": assessment.constitution_type,
            "total_score": float(assessment.total_score),
            "assessment_date": str(assessment.assessment_date),
            "trend": assessment.trend,
            "scores": {
                s.dimension: float(s.score)
                for s in scores_result.scalars().all()
            },
        },
    }
