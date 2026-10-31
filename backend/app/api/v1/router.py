"""Gom các endpoint v1 thành một router thống nhất."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints_detection import router as detection_router
from app.api.v1.endpoints_health import router as health_router
from app.api.v1.endpoints_history import router as history_router
from app.api.v1.endpoints_metrics import router as metrics_router
from app.api.v1.endpoints_signs import router as signs_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(detection_router)
api_v1_router.include_router(signs_router)
api_v1_router.include_router(history_router)
api_v1_router.include_router(metrics_router)
