"""Fixtures và cấu hình kiểm thử pytest cho backend."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import Settings
from app.data.seed_signs import seed_catalog
from app.main import create_app
from app.ml.detector import RawDetection, TrafficSignDetector
from app.models.database import get_db
from app.models.entities import Base, ScanHistory, TrafficSign  # noqa: F401


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        app_name="TrafficSign AI (Test)",
        environment="test",
        database_url="sqlite:///:memory:",
        max_upload_mb=1.0,  # 1 MB cho test
        min_image_side=32,
        max_image_side=2000,
        confidence_threshold=0.25,
        verification_threshold=0.5,
        catalog_auto_seed=False,
    )


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def in_memory_db(test_engine) -> Generator[Session, None, None]:
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    with TestingSessionLocal() as session:
        catalog_path = Path(__file__).resolve().parents[1] / "data" / "signs_catalog.csv"
        seed_catalog(session, catalog_path)
        yield session


class MockDetector(TrafficSignDetector):
    """Detector giả lập để kiểm thử API độc lập không phụ thuộc file weights lớn."""

    def __init__(self, detections: list[RawDetection] | None = None, is_ready: bool = True) -> None:
        super().__init__(weights_path=Path("weights/dummy.pt"))
        self._mock_detections = detections if detections is not None else []
        self._is_loaded = is_ready
        self._names_map = {
            0: "P.102 - Cam di nguoc chieu",
            1: "P.103a - Cam o to",
            999: "lop_khong_co_trong_catalog",
        }

    def predict(
        self,
        image: np.ndarray,
        confidence_override: float | None = None,
    ) -> list[RawDetection]:
        if not self._is_loaded:
            from app.core.errors import ModelNotReadyError

            raise ModelNotReadyError("Model test chưa được nạp.")

        conf = confidence_override if confidence_override is not None else self.conf_threshold
        return [d for d in self._mock_detections if d.confidence >= conf]


@pytest.fixture
def mock_detector() -> MockDetector:
    detections = [
        RawDetection(
            class_id=0,
            class_name="cam_di_nguoc_chieu",
            confidence=0.92,
            x1=50.0,
            y1=40.0,
            x2=150.0,
            y2=140.0,
        ),
        RawDetection(
            class_id=1,
            class_name="cam_o_to",
            confidence=0.38,
            x1=200.0,
            y1=100.0,
            x2=300.0,
            y2=200.0,
        ),
    ]
    return MockDetector(detections=detections, is_ready=True)


@pytest.fixture
def client(
    test_settings: Settings,
    in_memory_db: Session,
    mock_detector: MockDetector,
) -> Generator[TestClient, None, None]:
    app = create_app()

    def override_get_db() -> Generator[Session, None, None]:
        yield in_memory_db

    app.dependency_overrides[get_db] = override_get_db
    app.state.detector = mock_detector

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def valid_jpeg_bytes() -> bytes:
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.circle(img, (100, 100), 40, (0, 0, 255), -1)
    success, encoded = cv2.imencode(".jpg", img)
    assert success
    return encoded.tobytes()


@pytest.fixture
def valid_png_bytes() -> bytes:
    img = np.ones((300, 300, 3), dtype=np.uint8) * 200
    cv2.rectangle(img, (50, 50), (150, 150), (255, 0, 0), -1)
    success, encoded = cv2.imencode(".png", img)
    assert success
    return encoded.tobytes()


@pytest.fixture
def fake_jpg_text_bytes() -> bytes:
    return b"This is a plain text file pretending to be an image.jpg"


@pytest.fixture
def corrupted_image_bytes() -> bytes:
    return b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\x60\x00\x60\x00\x00corrupted"
