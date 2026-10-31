"""Endpoint kiểm tra trạng thái sức khỏe backend và model (API_SPEC §7.5)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request

from app.core.config import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(request: Request) -> dict[str, Any]:
    detector = getattr(request.app.state, "detector", None)
    model_loaded = detector.is_loaded if detector else False
    settings = get_settings()

    return {
        "status": "ok",
        "model_loaded": model_loaded,
        "model_version": settings.model_version,
        "dataset_version": settings.dataset_version,
        "device": settings.device,
        "history_enabled": settings.history_enabled,
        "max_upload_mb": settings.max_upload_mb,
        "confidence_range": {
            "min": settings.min_client_confidence,
            "max": settings.max_client_confidence,
            "default": settings.confidence_threshold,
            "verification_threshold": settings.verification_threshold,
        },
        "supported_formats": ["image/jpeg", "image/png"],
    }
