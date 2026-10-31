"""Cấu hình logging và middleware gắn request_id cho mỗi yêu cầu."""

from __future__ import annotations

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger("app.request")


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    )
    # Ultralytics in log khá nhiều ở mỗi lần predict; giữ ở WARNING.
    logging.getLogger("ultralytics").setLevel(logging.WARNING)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Sinh request_id, đo thời gian và chặn sớm body vượt giới hạn.

    Starlette đọc toàn bộ multipart trước khi vào handler, vì vậy kiểm tra
    `Content-Length` ở đây giúp từ chối file quá lớn mà không cần đọc hết.
    """

    # Phần dư cho boundary và các field form khác ngoài file.
    MULTIPART_OVERHEAD = 64 * 1024

    def __init__(self, app, max_body_bytes: int) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.max_body_bytes = max_body_bytes

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start = time.perf_counter()

        content_length = request.headers.get("content-length")
        if content_length and content_length.isdigit():
            if int(content_length) > self.max_body_bytes + self.MULTIPART_OVERHEAD:
                max_mb = self.max_body_bytes / (1024 * 1024)
                response: Response = JSONResponse(
                    status_code=413,
                    content={
                        "error": {
                            "code": "FILE_TOO_LARGE",
                            "message": f"Ảnh vượt quá giới hạn {max_mb:g} MB.",
                        },
                        "request_id": request_id,
                    },
                )
                response.headers["X-Request-ID"] = request_id
                return response

        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "%s %s -> %s (%.1f ms) request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
            request_id,
        )
        return response
