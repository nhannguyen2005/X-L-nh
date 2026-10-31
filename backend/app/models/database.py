"""Khởi tạo engine, session và dependency database."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.models.entities import Base

settings = get_settings()

# Đảm bảo thư mục data/ tồn tại khi dùng SQLite file
if settings.database_url.startswith("sqlite:///"):
    db_path = settings.database_url.replace("sqlite:///", "")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    echo=(settings.log_level.upper() == "DEBUG"),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Tạo tất cả các bảng nếu chưa có."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency cung cấp session SQLAlchemy cho FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
