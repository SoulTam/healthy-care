from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.user.schemas import (
    SendCodeRequest,
    LoginRequest,
    LoginPasswordRequest,
    RegisterRequest,
    ResetPasswordRequest,
    RefreshTokenRequest,
    WechatLoginRequest,
)
from app.user.service import user_service

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])


@router.post("/send-code")
async def send_code(req: SendCodeRequest):
    code = await user_service.send_code(req.phone)
    return {
        "code": "OK",
        "message": "验证码已发送",
        "data": {"code": code},
    }


@router.post("/register")
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await user_service.register(
        db, req.phone, req.code, req.password, req.nickname
    )
    return {"code": "OK", "message": "注册成功", "data": result}


@router.post("/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await user_service.login(db, req.phone, req.code)
    return {"code": "OK", "message": "登录成功", "data": result}


@router.post("/login-password")
async def login_password(
    req: LoginPasswordRequest, db: AsyncSession = Depends(get_db)
):
    result = await user_service.login_password(db, req.phone, req.password)
    return {"code": "OK", "message": "登录成功", "data": result}


@router.post("/reset-password")
async def reset_password(
    req: ResetPasswordRequest, db: AsyncSession = Depends(get_db)
):
    await user_service.reset_password(db, req.phone, req.code, req.new_password)
    return {"code": "OK", "message": "密码已重置"}


@router.post("/refresh")
async def refresh(req: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    result = await user_service.refresh_token(db, req.refresh_token)
    return {"code": "OK", "message": "Token 已刷新", "data": result}


@router.post("/logout")
async def logout(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    token: str = Depends(lambda: None),
):
    await user_service.logout(db, token)
    return {"code": "OK", "message": "已退出登录"}


@router.post("/wechat-login")
async def wechat_login(
    req: WechatLoginRequest, db: AsyncSession = Depends(get_db)
):
    raise NotImplementedError("微信登录待实现")
