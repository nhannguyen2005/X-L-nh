"""Schemas cho lịch sử quét biển báo (DATABASE §8.3, API_SPEC §7.4)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class HistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: str
    original_filename: str
    created_at: datetime
    detection_count: int
    processing_ms: float
    result: dict[str, Any] | None = None


class HistoryListResponse(BaseModel):
    items: list[HistoryItem]
    total: int
    page: int
    page_size: int
    total_pages: int
