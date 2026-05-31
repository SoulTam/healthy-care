from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, delete, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.favorite.models import Favorite

router = APIRouter(prefix="/api/v1/favorite", tags=["收藏服务"])


class ToggleFavoriteRequest(BaseModel):
    target_type: str
    target_id: str


@router.get("/list")
async def list_favorites(
    target_type: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    query = select(Favorite).where(Favorite.user_id == user_id)
    count_query = select(sa_func.count()).select_from(Favorite).where(
        Favorite.user_id == user_id
    )

    if target_type:
        query = query.where(Favorite.target_type == target_type)
        count_query = count_query.where(Favorite.target_type == target_type)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(Favorite.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    favorites = result.scalars().all()

    return {
        "code": "OK",
        "data": [
            {
                "id": str(f.id),
                "target_type": f.target_type,
                "target_id": str(f.target_id),
                "created_at": str(f.created_at),
            }
            for f in favorites
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/toggle")
async def toggle_favorite(
    req: ToggleFavoriteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    target_id = uuid.UUID(req.target_id)

    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.target_type == req.target_type,
            Favorite.target_id == target_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        await db.delete(existing)
        return {"code": "OK", "message": "Unfavorited", "favorited": False}
    else:
        fav = Favorite(
            user_id=user_id,
            target_type=req.target_type,
            target_id=target_id,
        )
        db.add(fav)
        return {"code": "OK", "message": "Favorited", "favorited": True}


@router.get("/check")
async def check_favorite(
    target_type: str = Query(...),
    target_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = uuid.UUID(current_user["id"])
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.target_type == target_type,
            Favorite.target_id == uuid.UUID(target_id),
        )
    )
    return {
        "code": "OK",
        "data": {"favorited": result.scalar_one_or_none() is not None},
    }
