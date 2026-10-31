"""Repository lưu và đọc lịch sử quét ảnh (DATABASE §8.3)."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session

from app.models.entities import ScanHistory


class HistoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        request_id: str,
        original_filename: str,
        detection_count: int,
        processing_ms: float,
        result_payload: dict[str, Any],
    ) -> ScanHistory:
        history = ScanHistory(
            request_id=request_id,
            original_filename=original_filename,
            detection_count=detection_count,
            processing_ms=processing_ms,
            result_json=json.dumps(result_payload, ensure_ascii=False),
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def get_by_id(self, history_id: int) -> ScanHistory | None:
        return self.session.get(ScanHistory, history_id)

    def get_by_request_id(self, request_id: str) -> ScanHistory | None:
        stmt = select(ScanHistory).where(ScanHistory.request_id == request_id)
        return self.session.scalars(stmt).first()

    def delete_by_id(self, history_id: int) -> bool:
        history = self.session.get(ScanHistory, history_id)
        if not history:
            return False
        self.session.delete(history)
        self.session.commit()
        return True

    def clear_all(self) -> int:
        stmt = delete(ScanHistory)
        result = self.session.execute(stmt)
        self.session.commit()
        return result.rowcount or 0

    def list_history(
        self, page: int = 1, page_size: int = 20, q: str | None = None
    ) -> tuple[list[ScanHistory], int]:
        stmt = select(ScanHistory)
        if q and q.strip():
            term = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    ScanHistory.original_filename.ilike(term),
                    ScanHistory.result_json.ilike(term),
                    ScanHistory.request_id.ilike(term),
                )
            )

        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.session.scalar(total_stmt) or 0

        offset = (page - 1) * page_size
        stmt = stmt.order_by(ScanHistory.created_at.desc()).offset(offset).limit(page_size)
        items = list(self.session.scalars(stmt).all())
        return items, total
