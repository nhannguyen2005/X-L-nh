"""Endpoint xem lịch sử quét ảnh (API_SPEC §7.4)."""

from __future__ import annotations

import json
import math
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import NotFoundError
from app.models.database import get_db
from app.repositories.history_repo import HistoryRepository
from app.schemas.history import HistoryItem, HistoryListResponse

router = APIRouter(prefix="/history", tags=["History"])


def _to_history_item(item: Any) -> HistoryItem:
    res_dict = None
    if item.result_json:
        try:
            res_dict = json.loads(item.result_json)
        except Exception:
            res_dict = None

    return HistoryItem(
        id=item.id,
        request_id=item.request_id,
        original_filename=item.original_filename,
        created_at=item.created_at,
        detection_count=item.detection_count,
        processing_ms=item.processing_ms,
        result=res_dict,
    )


@router.get("", response_model=HistoryListResponse)
def get_scan_history(
    q: Annotated[str | None, Query(description="Tìm kiếm theo tên file, nhãn hoặc request_id")] = None,
    page: Annotated[int, Query(ge=1, description="Số trang")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Số bản ghi mỗi trang")] = 20,
    db: Session = Depends(get_db),
) -> HistoryListResponse:
    settings = get_settings()
    page_size = min(page_size, settings.history_max_page_size)

    repo = HistoryRepository(db)
    items, total = repo.list_history(page=page, page_size=page_size, q=q)
    total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1

    return HistoryListResponse(
        items=[_to_history_item(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{history_id}", response_model=HistoryItem)
def get_scan_history_by_id(
    history_id: int,
    db: Session = Depends(get_db),
) -> HistoryItem:
    repo = HistoryRepository(db)
    item = repo.get_by_id(history_id)
    if not item:
        raise NotFoundError(f"Không tìm thấy bản ghi lịch sử với ID {history_id}.")
    return _to_history_item(item)


@router.delete("/{history_id}")
def delete_scan_history_by_id(
    history_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    repo = HistoryRepository(db)
    deleted = repo.delete_by_id(history_id)
    if not deleted:
        raise NotFoundError(f"Không tìm thấy bản ghi lịch sử với ID {history_id}.")
    return {"message": "Đã xóa bản ghi lịch sử thành công.", "id": history_id}


@router.delete("")
def clear_scan_history(
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    repo = HistoryRepository(db)
    count = repo.clear_all()
    return {"message": "Đã xóa toàn bộ lịch sử quét.", "deleted_count": count}
