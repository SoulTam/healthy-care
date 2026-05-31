from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.user.models import User, UserSession


_verification_codes: dict[str, dict] = {}


class UserService:
    async def send_code(self, phone: str) -> str:
        code = "123456"
        _verification_codes[phone] = {
            "code": code,
            "expires_at": datetime.now(timezone.utc)
            + timedelta(minutes=5),
        }
        return code

    def _verify_code(self, phone: str, code: str) -> bool:
        record = _verification_codes.get(phone)
        if not record:
            return False
        if datetime.now(timezone.utc) > record["expires_at"]:
            del _verification_codes[phone]
            return False
        if record["code"] != code:
            return False
        del _verification_codes[phone]
        return True

    async def register(
        self, db: AsyncSession, phone: str, code: str, password: str, nickname: str | None = None
    ) -> dict:
        if not self._verify_code(phone, code):
            raise HTTPException(status_code=400, detail="验证码错误或已过期")

        existing = await db.execute(select(User).where(User.phone == phone))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="手机号已注册")

        user = User(
            id=uuid.uuid4(),
            phone=phone,
            password_hash=hash_password(password),
            nickname=nickname or phone,
        )
        db.add(user)
        await db.flush()

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        session = UserSession(
            user_id=user.id,
            token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )
        db.add(session)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 1800,
            "user": {"id": str(user.id), "phone": user.phone, "nickname": user.nickname},
        }

    async def login(
        self, db: AsyncSession, phone: str, code: str
    ) -> dict:
        if not self._verify_code(phone, code):
            raise HTTPException(status_code=400, detail="验证码错误或已过期")

        result = await db.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        if user.status != "active":
            raise HTTPException(status_code=403, detail="账号已禁用")

        return await self._create_session(db, user)

    async def login_password(
        self, db: AsyncSession, phone: str, password: str
    ) -> dict:
        result = await db.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        if user.status != "active":
            raise HTTPException(status_code=403, detail="账号已禁用")

        if not user.password_hash or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="密码错误")

        return await self._create_session(db, user)

    async def _create_session(self, db: AsyncSession, user: User) -> dict:
        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        session = UserSession(
            user_id=user.id,
            token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
        db.add(session)

        user.last_login_at = datetime.now(timezone.utc)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 1800,
            "user": {"id": str(user.id), "phone": user.phone, "nickname": user.nickname},
        }

    async def refresh_token(
        self, db: AsyncSession, refresh_token: str
    ) -> dict:
        payload = decode_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="无效的 refresh_token")

        user_id = payload.get("sub")
        result = await db.execute(
            select(UserSession).where(
                UserSession.refresh_token == refresh_token,
                UserSession.expires_at > datetime.now(timezone.utc),
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=401, detail="refresh_token 已过期")

        new_access = create_access_token(user_id)
        new_refresh = create_refresh_token(user_id)
        session.token = new_access
        session.refresh_token = new_refresh

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "token_type": "bearer",
            "expires_in": 1800,
        }

    async def logout(self, db: AsyncSession, token: str) -> None:
        result = await db.execute(
            select(UserSession).where(UserSession.token == token)
        )
        session = result.scalar_one_or_none()
        if session:
            await db.delete(session)

    async def reset_password(
        self, db: AsyncSession, phone: str, code: str, new_password: str
    ) -> None:
        if not self._verify_code(phone, code):
            raise HTTPException(status_code=400, detail="验证码错误或已过期")

        result = await db.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        user.password_hash = hash_password(new_password)

    async def get_user_by_id(self, db: AsyncSession, user_id: str) -> User | None:
        result = await db.execute(
            select(User).where(User.id == uuid.UUID(user_id))
        )
        return result.scalar_one_or_none()


user_service = UserService()
