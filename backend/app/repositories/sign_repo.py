"""Repository truy vấn dữ liệu biển báo từ database."""

from __future__ import annotations

from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.entities import TrafficSign


class SignRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, sign_id: int) -> TrafficSign | None:
        return self.session.get(TrafficSign, sign_id)

    def get_by_class_id(self, class_id: int) -> TrafficSign | None:
        stmt = select(TrafficSign).where(TrafficSign.class_id == class_id)
        return self.session.scalars(stmt).first()

    def get_by_code(self, sign_code: str) -> TrafficSign | None:
        stmt = select(TrafficSign).where(TrafficSign.sign_code == sign_code)
        return self.session.scalars(stmt).first()

    def get_all_mapping(self) -> dict[int, TrafficSign]:
        """Lấy toàn bộ map {class_id: TrafficSign} để cache tra cứu lúc detection."""
        stmt = select(TrafficSign)
        signs = self.session.scalars(stmt).all()
        return {s.class_id: s for s in signs}

    def get_all_code_mapping(self) -> dict[str, TrafficSign]:
        """Lấy toàn bộ map {sign_code: TrafficSign} để tra cứu theo mã biển (P.112, etc.)."""
        stmt = select(TrafficSign)
        signs = self.session.scalars(stmt).all()
        return {s.sign_code: s for s in signs}

    def list_signs(
        self,
        q: str | None = None,
        group: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[TrafficSign], int]:
        stmt = select(TrafficSign)

        if q and q.strip():
            term = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    TrafficSign.name.ilike(term),
                    TrafficSign.sign_code.ilike(term),
                    TrafficSign.meaning.ilike(term),
                )
            )

        if group and group.strip():
            stmt = stmt.where(TrafficSign.group_name == group.strip())

        # Đếm tổng
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.session.scalar(count_stmt) or 0

        # Phân trang và sắp xếp theo class_id
        offset = (page - 1) * page_size
        stmt = stmt.order_by(TrafficSign.class_id.asc()).offset(offset).limit(page_size)
        items = list(self.session.scalars(stmt).all())

        return items, total

    def get_groups(self) -> list[dict[str, Any]]:
        """Lấy danh sách các nhóm biển báo kèm số lượng biển mỗi nhóm."""
        stmt = (
            select(TrafficSign.group_name, func.count(TrafficSign.id).label("count"))
            .group_by(TrafficSign.group_name)
            .order_by(TrafficSign.group_name.asc())
        )
        rows = self.session.execute(stmt).all()
        return [{"group_name": r[0], "count": r[1]} for r in rows]
