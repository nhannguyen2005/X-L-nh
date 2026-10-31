"""Dịch vụ nghiệp vụ tra cứu và tìm kiếm biển báo từ catalog."""

from __future__ import annotations

import math

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.entities import TrafficSign
from app.repositories.sign_repo import SignRepository
from app.schemas.sign import SignDetail, SignGroupSummary, SignListResponse, SignResponse


class CatalogService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repo = SignRepository(session)

    def get_sign_by_id(self, sign_id: int) -> SignDetail:
        sign = self.repo.get_by_id(sign_id)
        if not sign:
            raise NotFoundError(f"Không tìm thấy biển báo với ID {sign_id}.")
        return SignDetail.model_validate(sign)

    def get_sign_by_code(self, sign_code: str) -> SignDetail:
        sign = self.repo.get_by_code(sign_code)
        if not sign:
            raise NotFoundError(f"Không tìm thấy biển báo với mã '{sign_code}'.")
        return SignDetail.model_validate(sign)

    def list_signs(
        self,
        q: str | None = None,
        group: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> SignListResponse:
        page = max(1, page)
        page_size = max(1, min(page_size, 100))

        items, total = self.repo.list_signs(q=q, group=group, page=page, page_size=page_size)
        total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1

        return SignListResponse(
            items=[SignResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def get_groups(self) -> list[SignGroupSummary]:
        groups = self.repo.get_groups()
        return [SignGroupSummary(**g) for g in groups]

    def get_cached_catalog_map(self) -> dict[int, TrafficSign]:
        return self.repo.get_all_mapping()
