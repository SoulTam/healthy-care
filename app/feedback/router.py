from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.feedback.models import UserFeedback
from engine.llm.client import llm_client

router = APIRouter(prefix="/api/v1/feedback", tags=["反馈闭环"])


class SubmitFeedbackRequest(BaseModel):
    plan_id: str | None = None
    rating: int = 3
    symptoms_before: list[str] = []
    symptoms_after: list[str] = []
    comments: str | None = None


@router.post("/submit")
async def submit_feedback(
    req: SubmitFeedbackRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    feedback = UserFeedback(
        user_id=user_id,
        plan_id=uuid.UUID(req.plan_id) if req.plan_id else None,
        rating=req.rating,
        symptoms_before=req.symptoms_before,
        symptoms_after=req.symptoms_after,
        comments=req.comments,
    )
    db.add(feedback)
    return {"code": "OK", "message": "反馈已提交"}


@router.get("/history")
async def get_feedback_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    query = (
        select(UserFeedback)
        .where(UserFeedback.user_id == user_id)
        .order_by(UserFeedback.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    feedbacks = result.scalars().all()

    count_result = await db.execute(
        select(sa_func.count()).select_from(UserFeedback).where(
            UserFeedback.user_id == user_id
        )
    )

    return {
        "code": "OK",
        "data": [
            {
                "id": str(f.id),
                "rating": f.rating,
                "symptoms_before": f.symptoms_before,
                "symptoms_after": f.symptoms_after,
                "comments": f.comments,
                "created_at": str(f.created_at),
            }
            for f in feedbacks
        ],
        "total": count_result.scalar() or 0,
        "page": page,
        "page_size": page_size,
    }


@router.post("/interpret")
async def interpret_feedback(
    feedback_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(UserFeedback).where(UserFeedback.id == uuid.UUID(feedback_id))
    )
    feedback = result.scalar_one_or_none()
    if not feedback:
        return {"code": "NOT_FOUND", "message": "反馈不存在"}

    prompt = f"""分析以下用户反馈：
评分：{feedback.rating}/5
反馈前症状：{feedback.symptoms_before}
反馈后症状：{feedback.symptoms_after}
评论：{feedback.comments}

请分析用户的改善情况，以JSON格式返回。"""

    analysis = await llm_client.generate(prompt=prompt, temperature=0.3)

    return {
        "code": "OK",
        "data": {"analysis": analysis},
    }
