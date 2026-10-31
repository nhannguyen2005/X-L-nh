"""Script và hàm seed dữ liệu biển báo từ file CSV vào Database (DATABASE §8.6).

Hỗ trợ chạy idempotent (upsert theo sign_code/class_id), không tạo bản ghi trùng lặp.
"""

from __future__ import annotations

import csv
import logging
from datetime import date, datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.database import SessionLocal, init_db
from app.models.entities import TrafficSign

logger = logging.getLogger(__name__)


def seed_catalog(session: Session, csv_path: Path | None = None) -> int:
    """Đọc file CSV catalog và upsert vào bảng traffic_signs."""
    if csv_path is None:
        csv_path = get_settings().catalog_path

    if not csv_path.exists():
        logger.warning("Không tìm thấy file catalog tại %s. Bỏ qua seed.", csv_path)
        return 0

    count = 0
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            class_id = int(row["class_id"].strip())
            sign_code = row["sign_code"].strip()
            name = row["name"].strip()
            group_name = row["group_name"].strip()
            meaning = row["meaning"].strip()
            recommended_action = row["recommended_action"].strip()
            warning_level = row.get("warning_level", "info").strip() or "info"
            image_url = row.get("image_url", "").strip() or None
            legal_source = row.get("legal_source", "QCVN 41:2019/BGTVT").strip()
            checked_at_str = row.get("source_checked_at", "2026-10-30").strip()
            try:
                checked_at = date.fromisoformat(checked_at_str)
            except ValueError:
                checked_at = date.today()

            stmt = select(TrafficSign).where(
                (TrafficSign.sign_code == sign_code) | (TrafficSign.class_id == class_id)
            )
            existing = session.scalars(stmt).first()

            if existing:
                existing.class_id = class_id
                existing.sign_code = sign_code
                existing.name = name
                existing.group_name = group_name
                existing.meaning = meaning
                existing.recommended_action = recommended_action
                existing.warning_level = warning_level
                existing.image_url = image_url
                existing.legal_source = legal_source
                existing.source_checked_at = checked_at
                existing.updated_at = datetime.now()
            else:
                new_sign = TrafficSign(
                    class_id=class_id,
                    sign_code=sign_code,
                    name=name,
                    group_name=group_name,
                    meaning=meaning,
                    recommended_action=recommended_action,
                    warning_level=warning_level,
                    image_url=image_url,
                    legal_source=legal_source,
                    source_checked_at=checked_at,
                )
                session.add(new_sign)
            count += 1

    session.commit()
    return count


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    init_db()
    with SessionLocal() as session:
        seeded = seed_catalog(session)
        print(f"Seed hoàn tất: {seeded} biển báo.")


if __name__ == "__main__":
    main()
