"""Lỗi nghiệp vụ có cấu trúc và handler chuyển thành JSON theo API_SPEC §7.6.

Không bao giờ trả stack trace hay đường dẫn nội bộ cho client.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Lỗi có mã ổn định để frontend ánh xạ thông điệp."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


class InvalidImageError(AppError):
    def __init__(self, message: str = "Không thể đọc ảnh được tải lên.") -> None:
        super().__init__(400, "INVALID_IMAGE", message)


class FileTooLargeError(AppError):
    def __init__(self, max_mb: float) -> None:
        super().__init__(413, "FILE_TOO_LARGE", f"Ảnh vượt quá giới hạn {max_mb:g} MB.")


class UnsupportedMediaTypeError(AppError):
    def __init__(self, message: str = "Chỉ hỗ trợ ảnh JPG/JPEG hoặc PNG.") -> None:
        super().__init__(415, "UNSUPPORTED_MEDIA_TYPE", message)


class InvalidParameterError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(422, "INVALID_PARAMETER", message)


class InferenceError(AppError):
    def __init__(self, message: str = "Đã xảy ra lỗi khi phân tích ảnh.") -> None:
        super().__init__(500, "INFERENCE_ERROR", message)


class ModelNotReadyError(AppError):
    def __init__(self, message: str = "Model chưa sẵn sàng.") -> None:
        super().__init__(503, "MODEL_NOT_READY", message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Không tìm thấy tài nguyên.", code: str = "NOT_FOUND") -> None:
        super().__init__(404, code, message)


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def error_response(request: Request, status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {"code": code, "message": message},
            "request_id": _request_id(request),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(request: Request, exc: AppError) -> JSONResponse:
        log = logger.warning if exc.status_code < 500 else logger.error
        log(
            "AppError %s (%s) request_id=%s",
            exc.code,
            exc.status_code,
            _request_id(request),
        )
        return error_response(request, exc.status_code, exc.code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def _validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        fields = []
        for err in exc.errors():
            loc = [str(part) for part in err.get("loc", ()) if part not in ("body", "query", "path")]
            fields.append(".".join(loc) or "request")
        detail = ", ".join(sorted(set(fields)))
        message = f"Tham số không hợp lệ: {detail}." if detail else "Tham số không hợp lệ."
        return error_response(request, 422, "INVALID_PARAMETER", message)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        if exc.status_code == 404:
            return error_response(request, 404, "NOT_FOUND", "Không tìm thấy tài nguyên.")
        if exc.status_code == 405:
            return error_response(request, 405, "METHOD_NOT_ALLOWED", "Phương thức không được hỗ trợ.")
        return error_response(request, exc.status_code, "HTTP_ERROR", "Yêu cầu không hợp lệ.")

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error request_id=%s", _request_id(request))
        return error_response(request, 500, "INTERNAL_ERROR", "Đã xảy ra lỗi không mong muốn ở máy chủ.")
