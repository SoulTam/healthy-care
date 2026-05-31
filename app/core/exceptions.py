from __future__ import annotations

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request


class AppException(HTTPException):
    def __init__(self, code: str, message: str, detail: str | None = None):
        super().__init__(status_code=400)
        self.code = code
        self.message = message
        self.detail = detail


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(code="NOT_FOUND", message=message, status_code=404)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(code="UNAUTHORIZED", message=message, status_code=401)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(code="FORBIDDEN", message=message, status_code=403)


class ValidationException(AppException):
    def __init__(self, message: str, detail: str | None = None):
        super().__init__(code="VALIDATION_ERROR", message=message, detail=detail)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "detail": exc.detail,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": "HTTP_ERROR",
            "message": exc.detail,
        },
    )
