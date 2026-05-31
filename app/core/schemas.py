from __future__ import annotations

from pydantic import BaseModel


class ResponseModel(BaseModel):
    code: str = "OK"
    message: str = "Success"
    data: object | None = None


class PaginatedResponse(BaseModel):
    code: str = "OK"
    message: str = "Success"
    data: list | None = None
    total: int = 0
    page: int = 1
    page_size: int = 20


class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: str | None = None
