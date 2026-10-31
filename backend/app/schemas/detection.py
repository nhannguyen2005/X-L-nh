"""Schemas cho request & response nhận diện biển báo (API_SPEC §7.1)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.sign import SignSummary


class BoundingBox(BaseModel):
    x1: float = Field(..., description="Tọa độ x góc trên bên trái (pixel ảnh gốc)")
    y1: float = Field(..., description="Tọa độ y góc trên bên trái (pixel ảnh gốc)")
    x2: float = Field(..., description="Tọa độ x góc dưới bên phải (pixel ảnh gốc)")
    y2: float = Field(..., description="Tọa độ y góc dưới bên phải (pixel ảnh gốc)")


class DetectionItem(BaseModel):
    class_id: int
    class_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox: BoundingBox
    sign: SignSummary | None = None
    verification_required: bool = False


class ImageMeta(BaseModel):
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    annotated_image: str = Field(..., description="URL hoặc data-uri của ảnh kết quả có bounding box")


class DetectionSummary(BaseModel):
    detection_count: int = Field(..., ge=0)
    processing_ms: float = Field(..., ge=0)


class DetectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    request_id: str
    status: str = "completed"
    image: ImageMeta
    summary: DetectionSummary
    detections: list[DetectionItem]
    warnings: list[str] = Field(default_factory=list)
