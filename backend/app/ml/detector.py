"""Detector wrapper cho mô hình nhận diện biển báo (MODEL_TRAINING §6.6, ARCHITECTURE §3.5).

Tách biệt hoàn toàn khỏi logic HTTP và Database.
Chịu trách nhiệm load model một lần, chạy suy luận và quy đổi tọa độ về ảnh gốc.
Hỗ trợ cả YOLO deep learning và Computer Vision detector chuyên biệt cho biển báo Việt Nam.
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from app.core.errors import ModelNotReadyError

logger = logging.getLogger(__name__)

# Danh sách nhãn lớp chuẩn của tập dữ liệu COCO (80 classes)
# Nếu model nạp vào chứa các lớp này (person, car, motorcycle...), đây là weights COCO tổng quát,
# KHÔNG ĐƯỢC ánh xạ nhầm người/xe cộ thành biển báo giao thông.
COCO_CLASSES: set[str] = {
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
}


@dataclass(frozen=True)
class RawDetection:
    class_id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float


def compute_iou(box_a: tuple[int, int, int, int], box_b: tuple[int, int, int, int]) -> float:
    """Tính Intersection-over-Union (IoU) giữa 2 box (x1, y1, x2, y2)."""
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    area_b = max(0, bx2 - bx1) * max(0, by2 - by1)
    union_area = area_a + area_b - inter_area

    if union_area <= 0:
        return 0.0
    return inter_area / float(union_area)


class TrafficSignDetector:
    """Class Detector bọc Ultralytics YOLO & CV Traffic Sign Engine."""

    def __init__(
        self,
        weights_path: Path,
        device: str = "cpu",
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        image_size: int = 640,
    ) -> None:
        self.weights_path = Path(weights_path)
        self.device = device
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.image_size = image_size
        self._model: Any = None
        self._is_loaded: bool = False
        self._names_map: dict[int, str] = {}
        self._is_coco_weights: bool = False

        # Cache templates và catalog mapping
        self._templates: dict[str, dict[str, Any]] = {}
        self._code_to_class_id: dict[str, int] = {}
        self._class_id_to_code: dict[int, str] = {}

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def _load_catalog_and_templates(self) -> None:
        """Nạp dữ liệu catalog và bộ 65 ảnh mẫu biển báo chuẩn vào memory."""
        root_dir = Path(__file__).resolve().parents[2]
        catalog_path = root_dir / "data" / "signs_catalog.csv"

        if catalog_path.exists():
            try:
                with open(catalog_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cid = int(row["class_id"])
                        code = str(row["sign_code"]).strip()
                        self._code_to_class_id[code] = cid
                        self._class_id_to_code[cid] = code
                logger.info("Đã nạp catalog %d biển báo cho Detector.", len(self._code_to_class_id))
            except Exception as e:
                logger.warning("Không thể đọc signs_catalog.csv: %s", e)

        # Nạp template biển báo từ static/signs
        signs_dir = root_dir / "static" / "signs"
        if not signs_dir.exists():
            # Thử thư mục frontend/public/signs nếu static/signs chưa có
            signs_dir = root_dir.parent / "frontend" / "public" / "signs"

        if signs_dir.exists():
            png_files = list(signs_dir.glob("*.png"))
            for p in png_files:
                code = p.stem
                tpl = cv2.imread(str(p))
                if tpl is None:
                    continue

                t64 = cv2.resize(tpl, (64, 64))
                t_gray = cv2.cvtColor(t64, cv2.COLOR_BGR2GRAY)
                t_hsv = cv2.cvtColor(t64, cv2.COLOR_BGR2HSV)
                hist = cv2.calcHist([t_hsv], [0, 1], None, [18, 16], [0, 180, 0, 256])
                cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)

                # Vùng biểu tượng bên trong (chiếm khoảng 60% trung tâm)
                inner = t_gray[12:52, 12:52]

                self._templates[code] = {
                    "gray": t_gray,
                    "inner": inner,
                    "hist": hist,
                    "group": code[0].upper(),  # 'P', 'W', 'R', 'I'
                }

            logger.info("Đã nạp %d template biển báo chuẩn vào memory.", len(self._templates))

    def load(self) -> bool:
        """Tải weights lên memory một lần duy nhất lúc khởi động."""
        self._load_catalog_and_templates()

        if not self.weights_path.exists() or self.weights_path.stat().st_size == 0:
            logger.warning(
                "Không tìm thấy file weights tại '%s'. Detector sẽ chạy ở chế độ Computer Vision chuyên dụng.",
                self.weights_path,
            )
            # Nếu có templates, detector vẫn sẵn sàng chạy chế độ CV!
            if self._templates:
                self._is_loaded = True
                self._is_coco_weights = True
                return True
            self._is_loaded = False
            self._model = None
            return False

        try:
            from ultralytics import YOLO

            logger.info(
                "Đang nạp model YOLO từ %s trên thiết bị %s...",
                self.weights_path,
                self.device,
            )
            model = YOLO(str(self.weights_path))
            self._model = model
            self._names_map = {int(k): str(v) for k, v in getattr(model, "names", {}).items()}

            # Kiểm tra xem weights có phải là generic COCO không
            has_coco = bool(set(self._names_map.values()).intersection(COCO_CLASSES))
            if has_coco:
                self._is_coco_weights = True
                logger.info(
                    "Weights là mô hình COCO tổng quát (%d lớp: person, car, motorcycle...). "
                    "Hệ thống phát hiện biển báo giao thông CV chuyên dụng được kích hoạt để đảm bảo "
                    "nhận diện chính xác biển báo Việt Nam và không gán nhầm người/xe thành biển báo.",
                    len(self._names_map),
                )
            else:
                self._is_coco_weights = False
                logger.info("Weights là mô hình huấn luyện chuyên biệt cho biển báo giao thông. Số lớp: %d", len(self._names_map))

            self._is_loaded = True
            return True
        except Exception:
            logger.exception("Lỗi khi nạp weights từ %s. Fallback về chế độ CV.", self.weights_path)
            if self._templates:
                self._is_loaded = True
                self._is_coco_weights = True
                return True
            self._is_loaded = False
            self._model = None
            return False

    def detect_signs_cv(
        self,
        image: np.ndarray,
        conf_threshold: float = 0.25,
    ) -> list[RawDetection]:
        """Thuật toán Computer Vision phát hiện và nhận dạng biển báo giao thông.

        Pipeline:
        1. Phân đoạn màu sắc trong không gian HSV: Đỏ (Biển Cấm/Nguy hiểm), Xanh (Hiệu lệnh/Chỉ dẫn), Vàng (Nguy hiểm).
        2. Lọc hình học đường bao (Contour Geometric Filtering): Tỷ lệ khung (aspect ratio), độ tròn (circularity), độ lồi (solidity).
        3. Khử trùng lặp vùng phát hiện (NMS).
        4. Đối sánh đa đặc trưng (Multi-feature Template Matching): Normalized Cross-Correlation + Biểu tượng lõi + Histogram màu.
        5. Quy đổi độ tin cậy và gán nhãn mã biển chuẩn QCVN 41:2019/BGTVT.
        """
        h_img, w_img = image.shape[:2]
        if h_img < 16 or w_img < 16 or not self._templates:
            return []

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 1. Mask màu Đỏ (wrap quanh hue 0 và 180)
        m_r1 = cv2.inRange(hsv, np.array([0, 60, 40]), np.array([10, 255, 255]))
        m_r2 = cv2.inRange(hsv, np.array([165, 60, 40]), np.array([180, 255, 255]))
        mask_red = m_r1 | m_r2

        # Mask màu Xanh Lam (cho biển Hiệu Lệnh R và Chỉ Dẫn I)
        mask_blue = cv2.inRange(hsv, np.array([95, 60, 40]), np.array([135, 255, 255]))

        # Mask màu Vàng (cho phần lõi biển Cảnh Báo Nguy Hiểm W)
        mask_yellow = cv2.inRange(hsv, np.array([15, 60, 50]), np.array([35, 255, 255]))

        candidate_boxes: list[tuple[int, int, int, int, str]] = []

        # --- Phân tích contours màu đỏ (Biển Cấm P và Biển Nguy Hiểm W) ---
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours_red:
            area = cv2.contourArea(cnt)
            if area < 60:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            aspect = w / float(h)
            if not (0.65 <= aspect <= 1.45):
                continue

            peri = cv2.arcLength(cnt, True)
            circ = (4 * np.pi * area / (peri * peri)) if peri > 0 else 0
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            solidity = (float(area) / hull_area) if hull_area > 0 else 0

            # Kiểm tra xem có màu vàng bên trong không (Biển W)
            roi_y = mask_yellow[y:y+h, x:x+w]
            yellow_ratio = (np.count_nonzero(roi_y) / float(w * h)) if (w * h) > 0 else 0

            if yellow_ratio > 0.08 and solidity > 0.45:
                candidate_boxes.append((x, y, w, h, "W"))
            elif circ > 0.32 and solidity > 0.65:
                candidate_boxes.append((x, y, w, h, "P"))

        # --- Phân tích contours màu xanh (Biển Hiệu Lệnh R và Chỉ Dẫn I) ---
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours_blue:
            area = cv2.contourArea(cnt)
            if area < 65:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            aspect = w / float(h)
            peri = cv2.arcLength(cnt, True)
            circ = (4 * np.pi * area / (peri * peri)) if peri > 0 else 0
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            solidity = (float(area) / hull_area) if hull_area > 0 else 0

            if 0.70 <= aspect <= 1.40 and circ > 0.35 and solidity > 0.70:
                candidate_boxes.append((x, y, w, h, "R"))
            elif 0.55 <= aspect <= 2.20 and solidity > 0.75 and area >= 120:
                candidate_boxes.append((x, y, w, h, "I"))

        # Khử trùng lặp box (Non-Maximum Suppression)
        filtered_candidates: list[tuple[int, int, int, int, str]] = []
        for cand in candidate_boxes:
            cx, cy, cw, ch, cgroup = cand
            box_c = (cx, cy, cx + cw, cy + ch)
            duplicate = False
            for prev in filtered_candidates:
                px, py, pw, ph, _ = prev
                box_p = (px, py, px + pw, py + ph)
                if compute_iou(box_c, box_p) > 0.35:
                    duplicate = True
                    break
            if not duplicate:
                filtered_candidates.append(cand)

        raw_detections: list[RawDetection] = []

        # Đối sánh mẫu (Template Matching) cho từng candidate
        for x, y, w, h, group in filtered_candidates:
            # Mở rộng 5% biên để bao trọn viền biển báo
            pad_x = int(w * 0.06)
            pad_y = int(h * 0.06)
            x1 = max(0, x - pad_x)
            y1 = max(0, y - pad_y)
            x2 = min(w_img, x + w + pad_x)
            y2 = min(h_img, y + h + pad_y)

            roi = image[y1:y2, x1:x2]
            if roi.shape[0] < 8 or roi.shape[1] < 8:
                continue

            roi_64 = cv2.resize(roi, (64, 64))
            roi_gray = cv2.cvtColor(roi_64, cv2.COLOR_BGR2GRAY)
            roi_hsv = cv2.cvtColor(roi_64, cv2.COLOR_BGR2HSV)
            inner_roi = roi_gray[12:52, 12:52]

            hist_roi = cv2.calcHist([roi_hsv], [0, 1], None, [18, 16], [0, 180, 0, 256])
            cv2.normalize(hist_roi, hist_roi, 0, 1, cv2.NORM_MINMAX)

            best_code: str | None = None
            best_score: float = -1.0

            for code, t_data in self._templates.items():
                if t_data["group"] != group:
                    continue

                s_ncc = float(cv2.matchTemplate(roi_gray, t_data["gray"], cv2.TM_CCOEFF_NORMED)[0][0])
                s_inner = float(cv2.matchTemplate(inner_roi, t_data["inner"], cv2.TM_CCOEFF_NORMED)[0][0])
                s_hist = float(cv2.compareHist(hist_roi, t_data["hist"], cv2.HISTCMP_CORREL))

                combined = 0.45 * s_ncc + 0.35 * s_inner + 0.20 * max(0.0, s_hist)
                if combined > best_score:
                    best_score = combined
                    best_code = code

            # Ngưỡng phát hiện hợp lệ để loại trừ nhiễu nền
            if best_code and best_score >= 0.28:
                # Quy đổi điểm đối sánh thành độ tin cậy từ 0.60 đến 0.98
                confidence = min(0.98, max(0.60, round(0.55 + (best_score - 0.28) * 1.8, 2)))

                if confidence >= conf_threshold:
                    cid = self._code_to_class_id.get(best_code, 0)
                    raw_detections.append(
                        RawDetection(
                            class_id=cid,
                            class_name=best_code,
                            confidence=round(confidence, 4),
                            x1=float(x1),
                            y1=float(y1),
                            x2=float(x2),
                            y2=float(y2),
                        )
                    )

        raw_detections.sort(key=lambda d: d.confidence, reverse=True)
        return raw_detections

    def predict(
        self,
        image: np.ndarray,
        confidence_override: float | None = None,
    ) -> list[RawDetection]:
        """Thực hiện suy luận trên ảnh BGR numpy array.

        Tọa độ trả về luôn quy về pixel của ảnh gốc (x1, y1, x2, y2).
        """
        if not self._is_loaded:
            raise ModelNotReadyError("Model nhận diện chưa được nạp hoặc file weights chưa sẵn sàng.")

        conf = confidence_override if confidence_override is not None else self.conf_threshold

        # Trường hợp weights là mô hình COCO tổng quát:
        # Không dùng YOLO COCO để tránh gán nhầm người/xe thành biển báo,
        # sử dụng Computer Vision Traffic Sign Detector chuyên biệt cho biển báo Việt Nam.
        if self._is_coco_weights or self._model is None:
            return self.detect_signs_cv(image, conf_threshold=conf)

        # Trường hợp model chuyên biệt cho biển báo giao thông:
        try:
            results = self._model.predict(
                source=image,
                conf=conf,
                iou=self.iou_threshold,
                imgsz=self.image_size,
                device=self.device,
                verbose=False,
            )

            detections: list[RawDetection] = []
            if results and len(results) > 0:
                res = results[0]
                boxes = res.boxes
                if boxes is not None and len(boxes) > 0:
                    coords = boxes.xyxy.cpu().numpy()
                    confs = boxes.conf.cpu().numpy()
                    cls_ids = boxes.cls.cpu().numpy()

                    h_orig, w_orig = image.shape[:2]

                    for i in range(len(confs)):
                        c_id = int(cls_ids[i])
                        score = float(confs[i])
                        x1, y1, x2, y2 = coords[i]

                        x1 = max(0.0, min(float(x1), float(w_orig)))
                        y1 = max(0.0, min(float(y1), float(h_orig)))
                        x2 = max(0.0, min(float(x2), float(w_orig)))
                        y2 = max(0.0, min(float(y2), float(h_orig)))

                        if x2 <= x1 or y2 <= y1:
                            continue

                        class_name = self._names_map.get(c_id, self._class_id_to_code.get(c_id, f"class_{c_id}"))

                        detections.append(
                            RawDetection(
                                class_id=c_id,
                                class_name=class_name,
                                confidence=round(score, 4),
                                x1=round(x1, 1),
                                y1=round(y1, 1),
                                x2=round(x2, 1),
                                y2=round(y2, 1),
                            )
                        )

            # Nếu YOLO chuyên biệt không tìm thấy biển báo, bổ trợ bằng CV detector
            if len(detections) == 0:
                cv_detections = self.detect_signs_cv(image, conf_threshold=conf)
                detections.extend(cv_detections)

            detections.sort(key=lambda d: d.confidence, reverse=True)
            return detections

        except Exception as e:
            if isinstance(e, ModelNotReadyError):
                raise
            logger.exception("Lỗi trong quá trình suy luận mô hình")
            from app.core.errors import InferenceError

            raise InferenceError(f"Lỗi suy luận mô hình: {e}") from e
