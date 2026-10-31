"""Endpoint tra cứu thông tin biển báo giao thông (API_SPEC §7.2, §7.3)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.sign import SignDetail, SignGroupSummary, SignListResponse
from app.services.catalog_service import CatalogService

router = APIRouter(prefix="/signs", tags=["Traffic Signs"])


@router.get("", response_model=SignListResponse)
def list_signs(
    q: Annotated[str | None, Query(description="Tìm kiếm theo tên, mã hoặc ý nghĩa")] = None,
    group: Annotated[str | None, Query(description="Lọc theo nhóm biển báo")] = None,
    page: Annotated[int, Query(ge=1, description="Số trang")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Số bản ghi mỗi trang")] = 20,
    db: Session = Depends(get_db),
) -> SignListResponse:
    service = CatalogService(db)
    return service.list_signs(q=q, group=group, page=page, page_size=page_size)


@router.get("/groups", response_model=list[SignGroupSummary])
def list_sign_groups(
    db: Session = Depends(get_db),
) -> list[SignGroupSummary]:
    """Trả về danh sách các nhóm biển báo kèm số lượng biển báo mỗi nhóm."""
    service = CatalogService(db)
    return service.get_groups()


@router.get("/code/{sign_code}", response_model=SignDetail)
def get_sign_by_code(
    sign_code: str,
    db: Session = Depends(get_db),
) -> SignDetail:
    """Tra cứu chi tiết biển báo theo mã biển (ví dụ: P.102, W.201a)."""
    service = CatalogService(db)
    return service.get_sign_by_code(sign_code)


@router.get("/{sign_id}", response_model=SignDetail)
def get_sign_by_id(
    sign_id: int,
    db: Session = Depends(get_db),
) -> SignDetail:
    service = CatalogService(db)
    return service.get_sign_by_id(sign_id)
