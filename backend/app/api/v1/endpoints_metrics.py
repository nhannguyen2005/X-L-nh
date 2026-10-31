"""Endpoint cung cấp số liệu đánh giá mô hình thực tế (TESTING_EVALUATION.md, UI_UX.md §14.7.4)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Response

from app.core.config import get_settings
from app.core.errors import NotFoundError

router = APIRouter(prefix="/metrics", tags=["Evaluation Metrics"])


@router.get("")
def get_evaluation_metrics() -> dict[str, Any]:
    """Đọc dữ liệu đánh giá từ file evaluation.json (nếu có).

    Tuyệt đối không tạo số liệu giả nếu chưa có kết quả đo trên test set độc lập.
    """
    settings = get_settings()
    eval_file = settings.metrics_dir / "evaluation.json"

    if not eval_file.exists():
        available_plots = []
        if settings.metrics_dir.exists():
            available_plots = sorted(
                [
                    p.name
                    for p in settings.metrics_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg")
                ]
            )
        return {
            "has_data": False,
            "message": "Chưa có kết quả đánh giá trên tập test độc lập. Dữ liệu sẽ hiển thị sau khi chạy evaluate.py.",
            "metrics": None,
            "available_plots": available_plots,
        }

    try:
        with eval_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        available_plots = sorted(
            [
                p.name
                for p in settings.metrics_dir.iterdir()
                if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg")
            ]
        )
        return {
            "has_data": True,
            "metrics": data,
            "available_plots": available_plots,
        }
    except Exception as e:
        return {
            "has_data": False,
            "message": f"Không thể đọc file evaluation.json: {e}",
            "metrics": None,
            "available_plots": [],
        }


@router.get("/plots/{plot_name}")
def get_evaluation_plot(plot_name: str) -> Response:
    """Trả về file ảnh biểu đồ đánh giá (confusion_matrix.png, PR_curve.png, v.v.)."""
    settings = get_settings()
    safe_name = Path(plot_name).name
    file_path = settings.metrics_dir / safe_name

    if not file_path.exists() or not file_path.is_file():
        raise NotFoundError(f"Không tìm thấy biểu đồ '{safe_name}'.", "PLOT_NOT_FOUND")

    # Xác định media type
    media_type = "image/png"
    if safe_name.endswith(".jpg") or safe_name.endswith(".jpeg"):
        media_type = "image/jpeg"

    with file_path.open("rb") as f:
        content = f.read()

    return Response(content=content, media_type=media_type)
