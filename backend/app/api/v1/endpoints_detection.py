"""Endpoint nhận diện biển báo từ ảnh upload (API_SPEC §7.1)."""

from __future__ import annotations

import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Request, Response, UploadFile
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import (
    InvalidParameterError,
    ModelNotReadyError,
    NotFoundError,
)
from app.models.database import get_db
from app.schemas.detection import DetectionResponse
from app.services.detection_service import DetectionService
from app.services.image_service import image_cache

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/detections", tags=["Detection"])


@router.post("", response_model=DetectionResponse)
async def detect_traffic_signs(
    request: Request,
    file: Annotated[UploadFile, File(description="File ảnh JPG hoặc PNG")],
    confidence: Annotated[float | None, Form(description="Ngưỡng confidence tùy chỉnh")] = None,
    save_history: Annotated[bool, Form(description="Lưu vào lịch sử quét hay không")] = False,
    db: Session = Depends(get_db),
) -> DetectionResponse:
    settings = get_settings()

    # 1. Kiểm tra tham số confidence nếu có
    if confidence is not None:
        if not (settings.min_client_confidence <= confidence <= settings.max_client_confidence):
            raise InvalidParameterError(
                f"Ngưỡng confidence phải nằm trong khoảng [{settings.min_client_confidence:g}, {settings.max_client_confidence:g}]."
            )

    # 2. Kiểm tra model sẵn sàng
    detector = getattr(request.app.state, "detector", None)
    if not detector or not detector.is_loaded:
        raise ModelNotReadyError(
            "Model nhận diện chưa được nạp hoặc file weights chưa sẵn sàng trên máy chủ."
        )

    # 3. Lấy request_id và đọc bytes
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    original_filename = file.filename or "uploaded_image.jpg"

    file_bytes = await file.read()

    # 4. Thực thi pipeline nhận diện
    service = DetectionService(session=db, detector=detector)
    return service.process_image(
        file_bytes=file_bytes,
        original_filename=original_filename,
        request_id=request_id,
        confidence_override=confidence,
        save_history=save_history,
    )


@router.get("/{request_id}/image")
def get_annotated_image(request_id: str) -> Response:
    """Trả về file ảnh JPEG kết quả từ RAM cache."""
    jpeg_bytes = image_cache.get(request_id)
    if not jpeg_bytes:
        raise NotFoundError(
            "Không tìm thấy ảnh kết quả hoặc ảnh đã hết hạn lưu tạm.",
            code="IMAGE_EXPIRED_OR_NOT_FOUND",
        )
    return Response(
        content=jpeg_bytes,
        media_type="image/jpeg",
        headers={"Cache-Control": "public, max-age=900"},
    )
