"""Letterbox và quy đổi tọa độ (IMAGE_PROCESSING.md §4.3).

Letterbox co ảnh giữ nguyên tỷ lệ khung hình rồi thêm padding cho đủ kích
thước vuông mà model yêu cầu. Box model trả về nằm trên ảnh letterbox, nên
phải trừ padding và chia lại tỉ lệ để ra tọa độ pixel trên ảnh gốc.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

PAD_COLOR = (114, 114, 114)  # màu padding chuẩn của họ YOLO


@dataclass(frozen=True)
class LetterboxInfo:
    """Thông tin cần thiết để đảo ngược phép letterbox."""

    scale: float
    pad_x: float
    pad_y: float
    original_width: int
    original_height: int
    target_size: int


def letterbox(image: np.ndarray, target_size: int) -> tuple[np.ndarray, LetterboxInfo]:
    """Co ảnh về khung vuông `target_size` mà không làm méo hình."""
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("letterbox yêu cầu ảnh 3 kênh")
    height, width = image.shape[:2]
    scale = min(target_size / width, target_size / height)
    new_w = max(1, round(width * scale))
    new_h = max(1, round(height * scale))

    interpolation = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
    resized = cv2.resize(image, (new_w, new_h), interpolation=interpolation)

    pad_x = (target_size - new_w) / 2
    pad_y = (target_size - new_h) / 2
    left, top = int(round(pad_x - 0.1)), int(round(pad_y - 0.1))
    right, bottom = target_size - new_w - left, target_size - new_h - top
    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=PAD_COLOR)

    info = LetterboxInfo(
        scale=scale,
        pad_x=float(left),
        pad_y=float(top),
        original_width=width,
        original_height=height,
        target_size=target_size,
    )
    return padded, info


def scale_boxes_to_original(boxes: np.ndarray, info: LetterboxInfo) -> np.ndarray:
    """Chuyển box `[x1, y1, x2, y2]` từ ảnh letterbox về ảnh gốc và kẹp trong biên."""
    if boxes.size == 0:
        return boxes.reshape(0, 4).astype(np.float32)
    out = boxes.astype(np.float32).copy()
    out[:, [0, 2]] = (out[:, [0, 2]] - info.pad_x) / info.scale
    out[:, [1, 3]] = (out[:, [1, 3]] - info.pad_y) / info.scale
    out[:, [0, 2]] = out[:, [0, 2]].clip(0, info.original_width)
    out[:, [1, 3]] = out[:, [1, 3]].clip(0, info.original_height)
    return out
