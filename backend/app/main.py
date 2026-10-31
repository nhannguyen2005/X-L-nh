"""Entry point ứng dụng FastAPI cho TrafficSign AI (ARCHITECTURE §3.1, §3.5)."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logging import RequestContextMiddleware, configure_logging
from app.data.seed_signs import seed_catalog
from app.ml.detector import TrafficSignDetector
from app.models.database import SessionLocal, init_db

logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    # 1. Cấu hình logging
    configure_logging(settings.log_level)
    logger.info("Khởi động %s trong môi trường %s...", settings.app_name, settings.environment)

    # 2. Khởi tạo cơ sở dữ liệu và seed catalog
    try:
        init_db()
        if settings.catalog_auto_seed:
            with SessionLocal() as db:
                count = seed_catalog(db, settings.catalog_path)
                logger.info("Catalog kiểm chứng đã sẵn sàng: %d bản ghi.", count)
    except Exception:
        logger.exception("Lỗi khi khởi tạo database hoặc seed catalog")

    # 3. Nạp model một lần duy nhất lúc khởi động (load-once pattern)
    if not getattr(app.state, "detector", None):
        detector = TrafficSignDetector(
            weights_path=settings.model_path,
            device=settings.device,
            conf_threshold=settings.confidence_threshold,
            iou_threshold=settings.iou_threshold,
            image_size=settings.image_size,
        )
        loaded = detector.load()
        if loaded:
            logger.info("Model nhận diện đã sẵn sàng phục vụ.")
        else:
            logger.warning(
                "Model chưa được nạp. Các yêu cầu /detections sẽ trả 503 MODEL_NOT_READY cho đến khi có file weights."
            )
        app.state.detector = detector

    yield

    logger.info("Đang tắt ứng dụng...")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="API nhận diện biển báo giao thông Việt Nam và giải thích ý nghĩa/cảnh báo bằng xử lý ảnh và học sâu.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Đăng ký xử lý lỗi chuẩn hóa
    register_exception_handlers(app)

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )

    # Middleware quản lý request ID và giới hạn upload sớm
    app.add_middleware(
        RequestContextMiddleware,
        max_body_bytes=settings.max_upload_bytes,
    )

    # Gắn routes v1
    app.include_router(api_v1_router, prefix=settings.api_prefix)

    @app.get("/", tags=["Root"])
    def root() -> dict[str, str]:
        return {
            "app": settings.app_name,
            "version": "1.0.0",
            "docs": "/docs",
            "api_v1": settings.api_prefix,
        }

    return app


app = create_app()
