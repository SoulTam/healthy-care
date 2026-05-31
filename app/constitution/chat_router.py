from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.constitution.chat_models import ConstitutionChatSession
from app.constitution.models import ConstitutionAssessment, AssessmentScore
from app.constitution.algorithm import calculate_scores, determine_constitution
from app.constitution.report_generator import generate_report
from engine.llm.client import llm_client

router = APIRouter(prefix="/api/v1/constitution", tags=["AI对话问诊"])

CHAT_SYSTEM_PROMPT = """你是一位专业的中医体质评估医师。你的任务是：
1. 通过多轮对话了解用户的身体状况
2. 询问用户的症状、生活习惯、饮食偏好等信息
3. 每次只问1-2个问题，不要一次性问太多
4. 保持专业、温和、耐心的态度
5. 当收集到足够信息后，告诉用户可以点击"完成评估"来获取结果

请记住，你不是在做一个简单的问卷，而是进行中医体质辨证。"""


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


@router.post("/chat")
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])

    if req.session_id:
        result = await db.execute(
            select(ConstitutionChatSession).where(
                ConstitutionChatSession.id == uuid.UUID(req.session_id),
                ConstitutionChatSession.user_id == user_id,
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=404, detail="对话会话不存在")
    else:
        session = ConstitutionChatSession(
            user_id=user_id, messages=[]
        )
        db.add(session)
        await db.flush()

    messages = session.messages or []
    messages.append({"role": "user", "content": req.message})

    async def event_stream():
        full_response = ""
        try:
            async for chunk in llm_client.generate_stream(
                prompt=req.message,
                system_prompt=CHAT_SYSTEM_PROMPT,
            ):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk, 'session_id': str(session.id)})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

        messages.append({"role": "assistant", "content": full_response})
        session.messages = messages

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-Id": str(session.id),
        },
    )


class AssessChatRequest(BaseModel):
    session_id: str


@router.post("/chat/assess")
async def assess_chat(
    req: AssessChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    result = await db.execute(
        select(ConstitutionChatSession).where(
            ConstitutionChatSession.id == uuid.UUID(req.session_id),
            ConstitutionChatSession.user_id == user_id,
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="对话会话不存在")

    messages_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in (session.messages or [])
    )

    analysis_prompt = f"""根据以下用户与中医师的对话，提取用户的症状特征，并映射到九种体质评分（每项0-100分）。

对话记录：
{messages_text}

请以JSON格式返回：
{{
    "scores": {{
        "气虚质": 分数,
        "阳虚质": 分数,
        ...
    }},
    "primary_constitution": "主体质类型",
    "key_symptoms": ["主要症状列表"],
    "analysis": "简短分析"
}}"""

    llm_result = await llm_client.generate(
        prompt=analysis_prompt,
        temperature=0.3,
    )

    try:
        analysis = json.loads(llm_result)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI 分析失败")

    scores = analysis.get("scores", {})
    constitution_type = analysis.get(
        "primary_constitution", determine_constitution(scores)
    )

    assessment = ConstitutionAssessment(
        user_id=user_id,
        constitution_type=constitution_type,
        total_score=scores.get(constitution_type, 0),
        source="chat",
        assessment_date=datetime.now(timezone.utc).date(),
        summary_report=generate_report(constitution_type, scores),
    )
    db.add(assessment)
    await db.flush()

    for dim, score in scores.items():
        db.add(AssessmentScore(
            assessment_id=assessment.id, dimension=dim, score=score
        ))

    session.status = "completed"
    session.completed_at = datetime.now(timezone.utc)

    return {
        "code": "OK",
        "data": {
            "assessment_id": str(assessment.id),
            "constitution_type": constitution_type,
            "scores": scores,
            "analysis": analysis.get("analysis", ""),
        },
    }
