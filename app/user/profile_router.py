from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.user.models import User
from app.user.dietary_models import UserDietaryRestriction

router = APIRouter(prefix="/api/v1/user", tags=["用户服务"])


class UpdateProfileRequest(BaseModel):
    nickname: str | None = None
    avatar_url: str | None = None
    gender: str | None = None
    birthday: str | None = None
    region: str | None = None


class DietaryRestrictionsRequest(BaseModel):
    allergies: list[str] = []
    religious: list[str] = []
    pregnancy: bool = False
    pregnancy_trimester: int | None = None
    other_restrictions: list[str] = []


@router.get("/profile")
async def get_profile(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user: User = current_user["user"]
    return {
        "code": "OK",
        "data": {
            "id": str(user.id),
            "phone": user.phone,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "gender": user.gender,
            "birthday": str(user.birthday) if user.birthday else None,
            "region": user.region,
            "font_size": user.font_size,
        },
    }


@router.put("/profile")
async def update_profile(
    req: UpdateProfileRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user: User = current_user["user"]
    update_data = req.model_dump(exclude_none=True)
    if update_data:
        await db.execute(
            update(User).where(User.id == user.id).values(**update_data)
        )
    return {"code": "OK", "message": "Profile updated"}


@router.get("/dietary-restrictions")
async def get_restrictions(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user: User = current_user["user"]
    result = await db.execute(
        select(UserDietaryRestriction).where(
            UserDietaryRestriction.user_id == user.id
        )
    )
    dr = result.scalar_one_or_none()
    if not dr:
        return {"code": "OK", "data": None}
    return {
        "code": "OK",
        "data": {
            "allergies": dr.allergies,
            "religious": dr.religious,
            "pregnancy": dr.pregnancy,
            "pregnancy_trimester": dr.pregnancy_trimester,
            "other_restrictions": dr.other_restrictions,
        },
    }


@router.put("/dietary-restrictions")
async def update_restrictions(
    req: DietaryRestrictionsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user: User = current_user["user"]
    result = await db.execute(
        select(UserDietaryRestriction).where(
            UserDietaryRestriction.user_id == user.id
        )
    )
    dr = result.scalar_one_or_none()
    if dr:
        for key, value in req.model_dump().items():
            setattr(dr, key, value)
    else:
        dr = UserDietaryRestriction(
            user_id=user.id, **req.model_dump()
        )
        db.add(dr)
    return {"code": "OK", "message": "Dietary restrictions updated"}


@router.delete("/delete")
async def delete_account(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user: User = current_user["user"]
    user.status = "deleted"
    return {"code": "OK", "message": "Account deleted"}
