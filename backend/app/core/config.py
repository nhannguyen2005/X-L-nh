"""Cấu hình ứng dụng, đọc từ biến môi trường hoặc file `.env`.

Mọi giá trị có thể thay đổi giữa các máy (đường dẫn model, ngưỡng, giới hạn
upload, CORS) đều nằm ở đây để không bị hardcode rải rác trong code.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        protected_namespaces=("settings_",),
    )

    app_name: str = "TrafficSign AI"
    api_prefix: str = "/api/v1"
    log_level: str = "INFO"

    # --- Model ---------------------------------------------------------------
    model_path: Path = BACKEND_DIR / "weights" / "best.pt"
    model_version: str = "unversioned"
    dataset_version: str = "unversioned"
    device: str = "cpu"
    image_size: int = Field(640, ge=160, le=1920)
    confidence_threshold: float = Field(0.25, gt=0, lt=1)
    iou_threshold: float = Field(0.45, gt=0, lt=1)
    # Detection có confidence dưới ngưỡng này được đánh dấu "cần xác minh".
    verification_threshold: float = Field(0.5, gt=0, lt=1)
    # Giới hạn cho tham số `confidence` do client gửi.
    min_client_confidence: float = Field(0.05, gt=0, lt=1)
    max_client_confidence: float = Field(0.95, gt=0, lt=1)
    max_detections: int = Field(50, ge=1, le=300)
    # Tiền xử lý thử nghiệm (ablation). Mặc định tắt theo IMAGE_PROCESSING.md.
    preprocess_clahe: bool = False

    # --- Upload ----------------------------------------------------------------
    max_upload_mb: float = Field(10, gt=0, le=50)
    max_image_side: int = Field(8000, ge=64)
    min_image_side: int = Field(32, ge=1)

    # --- Kết quả tạm (ảnh annotated giữ trong RAM) -------------------------------
    result_ttl_seconds: int = Field(900, ge=10)
    result_cache_size: int = Field(64, ge=1)

    # --- Dữ liệu ---------------------------------------------------------------
    database_url: str = f"sqlite:///{(BACKEND_DIR / 'data' / 'app.db').as_posix()}"
    catalog_path: Path = BACKEND_DIR / "data" / "signs_catalog.csv"
    catalog_auto_seed: bool = True
    history_enabled: bool = True
    history_max_page_size: int = Field(100, ge=1)

    # --- Đánh giá mô hình ------------------------------------------------------
    metrics_dir: Path = PROJECT_DIR / "artifacts" / "metrics"

    # --- HTTP ------------------------------------------------------------------
    cors_origins: Annotated[list[str], NoDecode] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    environment: Literal["development", "production", "test"] = "development"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip().startswith("["):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def _check_ranges(self) -> Settings:
        if self.min_client_confidence >= self.max_client_confidence:
            raise ValueError("MIN_CLIENT_CONFIDENCE phải nhỏ hơn MAX_CLIENT_CONFIDENCE")
        if not (self.min_client_confidence <= self.confidence_threshold <= self.max_client_confidence):
            raise ValueError("CONFIDENCE_THRESHOLD phải nằm trong khoảng cho phép của client")
        return self

    @property
    def max_upload_bytes(self) -> int:
        return int(self.max_upload_mb * 1024 * 1024)


@lru_cache
def get_settings() -> Settings:
    return Settings()
