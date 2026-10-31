"""Dịch vụ xử lý ảnh: validation, tiền xử lý và vẽ bounding box (IMAGE_PROCESSING.md)."""

from __future__ import annotations

import base64
import collections
import logging
import time
from typing import Any

import cv2
import numpy as np

from app.core.config import get_settings
from app.core.errors import (
    FileTooLargeError,
    InvalidImageError,
    UnsupportedMediaTypeError,
)

logger = logging.getLogger(__name__)

# BGR colors for sign groups
GROUP_COLORS_BGR: dict[str, tuple[int, int, int]] = {
    "Biển cấm": (46, 16, 200),  # Đỏ (#C8102E)
    "Biển nguy hiểm và cảnh báo": (5, 183, 242),  # Vàng (#F2B705)
    "Biển hiệu lệnh": (173, 92, 11),  # Xanh dương (#0B5CAD)
    "Biển chỉ dẫn": (138, 58, 30),  # Xanh thẫm (#1E3A8A)
}
DEFAULT_COLOR_BGR = (91, 82, 82)  # Xám cho unknown


class ImageCache:
    """Bộ nhớ đệm tạm thời cho ảnh annotated (TTL & dung lượng giới hạn trong RAM)."""

    def __init__(self, max_items: int = 64, ttl_seconds: int = 900) -> None:
        self.max_items = max_items
        self.ttl_seconds = ttl_seconds
        self._cache: collections.OrderedDict[str, tuple[bytes, float]] = collections.OrderedDict()

    def set(self, key: str, image_bytes: bytes) -> None:
        self._evict_expired()
        if len(self._cache) >= self.max_items:
            self._cache.popitem(last=False)
        self._cache[key] = (image_bytes, time.time())

    def get(self, key: str) -> bytes | None:
        self._evict_expired()
        item = self._cache.get(key)
        if item is None:
            return None
        # Đưa lên đầu LRU
        self._cache.move_to_end(key)
        return item[0]

    def _evict_expired(self) -> None:
        now = time.time()
        expired_keys = [k for k, (_, t) in self._cache.items() if now - t > self.ttl_seconds]
        for k in expired_keys:
            self._cache.pop(k, None)


# Khởi tạo singleton cache
image_cache = ImageCache(
    max_items=get_settings().result_cache_size,
    ttl_seconds=get_settings().result_ttl_seconds,
)


class ImageService:
    @staticmethod
    def validate_and_decode(file_bytes: bytes, filename: str | None = None) -> np.ndarray:
        """Xác thực kích thước, MIME magic bytes và giải mã thành ảnh BGR."""
        settings = get_settings()

        # 1. Kiểm tra dung lượng
        if len(file_bytes) > settings.max_upload_bytes:
            raise FileTooLargeError(settings.max_upload_mb)

        if len(file_bytes) < 16:
            raise InvalidImageError("Dữ liệu tệp quá nhỏ hoặc rỗng.")

        # 2. Kiểm tra magic bytes
        # JPEG: FF D8 FF
        # PNG: 89 50 4E 47 0D 0A 1A 0A
        is_jpeg = file_bytes.startswith(b"\xff\xd8\xff")
        is_png = file_bytes.startswith(b"\x89PNG\r\n\x1a\n")

        if not (is_jpeg or is_png):
            raise UnsupportedMediaTypeError("Chỉ hỗ trợ ảnh định dạng JPG/JPEG hoặc PNG.")

        # 3. Giải mã ảnh qua OpenCV
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None or image.size == 0:
            raise InvalidImageError("Không thể giải mã dữ liệu ảnh. Tệp có thể bị hỏng.")

        # 4. Kiểm tra kích thước
        h, w = image.shape[:2]
        if (
            w < settings.min_image_side
            or h < settings.min_image_side
            or w > settings.max_image_side
            or h > settings.max_image_side
        ):
            raise InvalidImageError(
                f"Kích thước ảnh ({w}x{h}) không hợp lệ. Cho phép từ {settings.min_image_side}px đến {settings.max_image_side}px."
            )

        return image

    @staticmethod
    def apply_clahe(image: np.ndarray) -> np.ndarray:
        """Thực hiện cân bằng sáng CLAHE trên kênh Luminance (IMAGE_PROCESSING §4.3)."""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_chan, a_chan, b_chan = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l_chan)
        limg = cv2.merge((cl, a_chan, b_chan))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    @staticmethod
    def annotate_image(
        image: np.ndarray,
        detections: list[dict[str, Any]],
    ) -> bytes:
        """Vẽ bounding box và nhãn lên bản sao ảnh, trả về JPEG bytes."""
        canvas = image.copy()
        h, w = canvas.shape[:2]

        # Tỷ lệ độ dày nét theo kích thước ảnh
        thickness = max(2, int(round(min(w, h) / 400)))
        font_scale = max(0.5, min(w, h) / 800)

        for idx, det in enumerate(detections, start=1):
            bbox = det["bbox"]
            x1, y1 = int(round(bbox["x1"])), int(round(bbox["y1"]))
            x2, y2 = int(round(bbox["x2"])), int(round(bbox["y2"]))

            sign_info = det.get("sign")
            group_name = sign_info.get("group") if sign_info else None
            color = GROUP_COLORS_BGR.get(group_name, DEFAULT_COLOR_BGR)

            # Vẽ bounding box
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, thickness)

            # Nhãn số thứ tự và confidence (ví dụ: "1: 93%")
            conf_pct = int(round(det["confidence"] * 100))
            label = f"{idx}: {conf_pct}%"

            (lw, lh), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            badge_y1 = max(0, y1 - lh - baseline - 4)
            badge_y2 = badge_y1 + lh + baseline + 4
            badge_x2 = min(w, x1 + lw + 8)

            # Nền badge
            cv2.rectangle(canvas, (x1, badge_y1), (badge_x2, badge_y2), color, -1)
            # Chữ trắng tương phản
            text_y = badge_y2 - baseline - 2
            cv2.putText(
                canvas,
                label,
                (x1 + 4, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                (255, 255, 255),
                max(1, thickness - 1),
                cv2.LINE_AA,
            )

        success, encoded = cv2.imencode(".jpg", canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        if not success:
            raise RuntimeError("Lỗi khi mã hóa ảnh annotated thành JPEG.")
        return encoded.tobytes()

    @staticmethod
    def to_base64_data_uri(jpeg_bytes: bytes) -> str:
        b64 = base64.b64encode(jpeg_bytes).decode("ascii")
        return f"data:image/jpeg;base64,{b64}"
