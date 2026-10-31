"""DetectionService điều phối toàn bộ pipeline nhận diện (ARCHITECTURE §3.4)."""

from __future__ import annotations

import logging
import time
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.ml.detector import TrafficSignDetector
from app.repositories.history_repo import HistoryRepository
from app.repositories.sign_repo import SignRepository
from app.schemas.detection import (
    BoundingBox,
    DetectionItem,
    DetectionResponse,
    DetectionSummary,
    ImageMeta,
)
from app.schemas.sign import SignSummary
from app.services.image_service import ImageService, image_cache

logger = logging.getLogger(__name__)


class DetectionService:
    def __init__(
        self,
        session: Session,
        detector: TrafficSignDetector,
    ) -> None:
        self.session = session
        self.detector = detector
        self.sign_repo = SignRepository(session)
        self.history_repo = HistoryRepository(session)
        self.settings = get_settings()

    def process_image(
        self,
        file_bytes: bytes,
        original_filename: str,
        request_id: str,
        confidence_override: float | None = None,
        save_history: bool = False,
    ) -> DetectionResponse:
        start_time = time.perf_counter()
        warnings: list[str] = []

        # 1. Validation & Decode
        image = ImageService.validate_and_decode(file_bytes, original_filename)
        h_orig, w_orig = image.shape[:2]

        # 2. Tiền xử lý thử nghiệm (nếu cấu hình)
        if self.settings.preprocess_clahe:
            image_for_model = ImageService.apply_clahe(image)
        else:
            image_for_model = image

        # 3. Model suy luận
        raw_detections = self.detector.predict(
            image_for_model,
            confidence_override=confidence_override,
        )

        # Giới hạn số lượng detection tối đa để tránh quá tải
        if len(raw_detections) > self.settings.max_detections:
            warnings.append(
                f"Số lượng phát hiện ({len(raw_detections)}) vượt giới hạn hiển thị. Đã giữ lại {self.settings.max_detections} kết quả có độ tin cậy cao nhất."
            )
            raw_detections = raw_detections[: self.settings.max_detections]

        # 4. Tra cứu catalog thông tin biển báo
        catalog_map = self.sign_repo.get_all_mapping()
        code_map = self.sign_repo.get_all_code_mapping()

        formatted_detections: list[DetectionItem] = []
        dict_detections_for_annotation: list[dict[str, Any]] = []

        from app.ml.detector import COCO_CLASSES

        for raw in raw_detections:
            # Loại bỏ hoàn toàn các lớp COCO không phải biển báo (person, car, motorcycle...)
            if raw.class_name.lower() in COCO_CLASSES:
                continue

            sign_entity = code_map.get(raw.class_name) or catalog_map.get(raw.class_id)
            sign_summary: SignSummary | None = None

            resolved_class_id = sign_entity.class_id if sign_entity else raw.class_id
            resolved_class_name = sign_entity.sign_code if sign_entity else raw.class_name

            if sign_entity:
                sign_summary = SignSummary(
                    id=sign_entity.id,
                    sign_code=sign_entity.sign_code,
                    name=sign_entity.name,
                    group=sign_entity.group_name,
                    meaning=sign_entity.meaning,
                    recommended_action=sign_entity.recommended_action,
                    warning_level=sign_entity.warning_level,  # type: ignore[arg-type]
                    source=sign_entity.legal_source,
                    source_checked_at=sign_entity.source_checked_at,
                    image_url=sign_entity.image_url,
                )
            else:
                warnings.append(
                    f"Nhãn lớp '{raw.class_name}' (ID: {raw.class_id}) chưa có bản ghi trong catalog kiểm chứng."
                )

            # Đánh dấu cần xác minh nếu confidence thấp hơn ngưỡng hoặc không có catalog
            verification_required = (
                raw.confidence < self.settings.verification_threshold or sign_summary is None
            )

            bbox = BoundingBox(
                x1=raw.x1,
                y1=raw.y1,
                x2=raw.x2,
                y2=raw.y2,
            )

            item = DetectionItem(
                class_id=resolved_class_id,
                class_name=resolved_class_name,
                confidence=raw.confidence,
                bbox=bbox,
                sign=sign_summary,
                verification_required=verification_required,
            )
            formatted_detections.append(item)

            dict_detections_for_annotation.append(
                {
                    "bbox": {"x1": raw.x1, "y1": raw.y1, "x2": raw.x2, "y2": raw.y2},
                    "confidence": raw.confidence,
                    "sign": sign_summary.model_dump() if sign_summary else None,
                }
            )


        # 5. Vẽ bounding box và lưu cache ảnh kết quả
        annotated_jpeg = ImageService.annotate_image(image, dict_detections_for_annotation)
        image_cache.set(request_id, annotated_jpeg)

        # 6. Đo thời gian xử lý
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 1)

        # 7. Lưu lịch sử nếu được yêu cầu
        if save_history and self.settings.history_enabled:
            try:
                minimal_result = {
                    "detection_count": len(formatted_detections),
                    "classes": [d.class_name for d in formatted_detections],
                    "processing_ms": elapsed_ms,
                }
                self.history_repo.create(
                    request_id=request_id,
                    original_filename=original_filename,
                    detection_count=len(formatted_detections),
                    processing_ms=elapsed_ms,
                    result_payload=minimal_result,
                )
            except Exception:
                logger.exception("Lỗi khi lưu lịch sử quét vào database")
                warnings.append("Không thể lưu kết quả vào lịch sử quét.")

        annotated_url = f"{self.settings.api_prefix}/detections/{request_id}/image"

        return DetectionResponse(
            request_id=request_id,
            status="completed",
            image=ImageMeta(
                width=w_orig,
                height=h_orig,
                annotated_image=annotated_url,
            ),
            summary=DetectionSummary(
                detection_count=len(formatted_detections),
                processing_ms=elapsed_ms,
            ),
            detections=formatted_detections,
            warnings=list(dict.fromkeys(warnings)),  # Khử trùng lặp cảnh báo
        )
