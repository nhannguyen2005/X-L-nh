"""Định nghĩa thực thể ORM SQLAlchemy (DATABASE §8.2, §8.3)."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TrafficSign(Base):
    __tablename__ = "traffic_signs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    sign_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    group_name: Mapped[str] = mapped_column(String(100), nullable=False)
    meaning: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)
    warning_level: Mapped[str] = mapped_column(String(20), nullable=False, default="info")
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    legal_source: Mapped[str] = mapped_column(String(255), nullable=False)
    source_checked_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def to_summary_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "sign_code": self.sign_code,
            "name": self.name,
            "group": self.group_name,
            "meaning": self.meaning,
            "recommended_action": self.recommended_action,
            "warning_level": self.warning_level,
            "source": self.legal_source,
            "source_checked_at": self.source_checked_at,
            "image_url": self.image_url,
        }


class ScanHistory(Base):
    __tablename__ = "scan_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), index=True)
    detection_count: Mapped[int] = mapped_column(Integer, nullable=False)
    processing_ms: Mapped[float] = mapped_column(Float, nullable=False)
    result_json: Mapped[str] = mapped_column(Text, nullable=False)
