from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class SendCodeRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\d{11}$")


class SendCodeResponse(BaseModel):
    code: str = "OK"
    message: str = "验证码已发送"
    data: dict | None = None


class LoginRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\d{11}$")
    code: str = Field(..., min_length=4, max_length=6)


class LoginPasswordRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\d{11}$")
    password: str = Field(..., min_length=6, max_length=128)


class RegisterRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\d{11}$")
    code: str = Field(..., min_length=4, max_length=6)
    password: str = Field(..., min_length=6, max_length=128)
    nickname: str | None = None


class ResetPasswordRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\d{11}$")
    code: str = Field(..., min_length=4, max_length=6)
    new_password: str = Field(..., min_length=6, max_length=128)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800


class WechatLoginRequest(BaseModel):
    code: str


class UserProfile(BaseModel):
    id: str
    phone: str
    nickname: str | None = None
    avatar_url: str | None = None
    gender: str = "other"
    birthday: datetime | None = None
    region: str | None = None
    font_size: str = "normal"
