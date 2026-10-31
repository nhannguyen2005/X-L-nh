"""Script tự động cắt ảnh biển báo từ các trang tài liệu scan (he-thong-bien-bao.md).

Và cập nhật dữ liệu chuẩn hóa vào backend/data/signs_catalog.csv cùng SQLite.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path

import cv2
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

WORKSPACE = Path("e:/xulyanh")
FRONTEND_SIGNS_DIR = WORKSPACE / "frontend" / "public" / "signs"
BACKEND_SIGNS_DIR = WORKSPACE / "backend" / "static" / "signs"
CATALOG_CSV_PATH = WORKSPACE / "backend" / "data" / "signs_catalog.csv"

FRONTEND_SIGNS_DIR.mkdir(parents=True, exist_ok=True)
BACKEND_SIGNS_DIR.mkdir(parents=True, exist_ok=True)


def extract_sign_graphic(cell: np.ndarray, pad: int = 4, min_area: int = 300) -> np.ndarray | None:
    """Tách phần đồ họa biển báo bằng phân tích độ bão hòa màu (saturation).

    Loại bỏ khung viền đen và chữ tiếng Việt ở đáy ô.
    """
    h, w, _ = cell.shape
    # Bỏ 2px viền ngoài của cell
    inner = cell[2 : h - 2, 2 : w - 2]
    ih, iw, _ = inner.shape

    hsv = cv2.cvtColor(inner, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]

    # Vùng có màu sắc (biển báo có màu đỏ, vàng, xanh, trắng bên trong)
    color_mask = (sat > 35) & (val > 35)

    # Nếu không tìm thấy màu (ví dụ biển phụ trắng đen), dùng ngưỡng nhị phân ở nửa trên
    if np.sum(color_mask) < 200:
        top_half = inner[: int(ih * 0.65), :]
        gray_top = cv2.cvtColor(top_half, cv2.COLOR_BGR2GRAY)
        mask_bw = gray_top < 220
        coords = np.argwhere(mask_bw)
        if len(coords) > 100:
            r0, c0 = coords.min(axis=0)
            r1, c1 = coords.max(axis=0) + 1
            r0 = max(0, r0 - pad)
            c0 = max(0, c0 - pad)
            r1 = min(top_half.shape[0], r1 + pad)
            c1 = min(top_half.shape[1], c1 + pad)
            return top_half[r0:r1, c0:c1]
        return None

    # Biển có màu: tìm các contour bao
    mask_u8 = color_mask.astype(np.uint8) * 255
    # Morph close để nối liền viền tròn / tam giác
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_closed = cv2.morphologyEx(mask_u8, cv2.MORPH_CLOSE, kernel)

    cnts, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_boxes = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area:
            valid_boxes.append(cv2.boundingRect(c))

    if not valid_boxes:
        return None

    # Lấy bbox bao toàn bộ các thành phần màu của biển
    min_x = min(b[0] for b in valid_boxes)
    min_y = min(b[1] for b in valid_boxes)
    max_x = max(b[0] + b[2] for b in valid_boxes)
    max_y = max(b[1] + b[3] for b in valid_boxes)

    x0 = max(0, min_x - pad)
    y0 = max(0, min_y - pad)
    x1 = min(iw, max_x + pad)
    y1 = min(ih, max_y + pad)

    crop = inner[y0:y1, x0:x1]
    return crop


def save_sign_images(sign_code: str, image: np.ndarray) -> str:
    """Lưu ảnh vào cả frontend public và backend static."""
    filename = f"{sign_code}.png"
    front_path = FRONTEND_SIGNS_DIR / filename
    back_path = BACKEND_SIGNS_DIR / filename
    cv2.imwrite(str(front_path), image)
    cv2.imwrite(str(back_path), image)
    return f"/signs/{filename}"


def main() -> None:
    p1 = cv2.imread(str(WORKSPACE / "images" / "page-1.png"))
    p2 = cv2.imread(str(WORKSPACE / "images" / "page-2.png"))
    p3 = cv2.imread(str(WORKSPACE / "images" / "page-3.png"))
    p4 = cv2.imread(str(WORKSPACE / "images" / "page-4.png"))

    # Định nghĩa cấu hình trích xuất cho từng biển
    # (page, y1, y2, x1, x2, sub_idx: index contour nếu ô có nhiều biển)
    EXTRACTION_MAP: dict[str, tuple[np.ndarray, int, int, int, int, int | None]] = {
        # --- 23 Lớp cốt lõi phát hiện mô hình ---
        # P.102: Cấm đi ngược chiều (Page 2 row 0 col 1)
        "P.102": (p2, 290, 483, 354, 508, None),
        # P.103a: Cấm ô tô (Page 2 row 0 col 6)
        "P.103a": (p2, 290, 483, 1126, 1280, None),
        # P.104: Cấm xe máy (Page 2 row 0 col 5 - Cấm xe mô tô 2-3 bánh)
        "P.104": (p2, 290, 483, 972, 1126, None),
        # P.112: Cấm người đi bộ (Page 2 row 0 col 2)
        "P.112": (p2, 290, 483, 508, 663, None),
        # P.123a: Cấm rẽ trái (Page 2 row 3 col 0)
        "P.123a": (p2, 849, 1044, 200, 354, None),
        # P.123b: Cấm rẽ phải (Page 2 row 3 col 2)
        "P.123b": (p2, 849, 1044, 508, 663, None),
        # P.124a: Cấm quay đầu xe (Page 2 row 3 col 4)
        "P.124a": (p2, 849, 1044, 817, 972, None),
        # P.127: Tốc độ tối đa cho phép (Page 2 row 6 col 0)
        "P.127": (p2, 1474, 1647, 200, 354, None),
        # P.130: Cấm dừng xe và đỗ xe (Page 2 row 6 col 3)
        "P.130": (p2, 1474, 1647, 663, 817, None),
        # P.131a: Cấm đỗ xe (Page 2 row 6 col 4)
        "P.131a": (p2, 1474, 1647, 817, 972, None),
        # W.201a: Chỗ ngoặt nguy hiểm vòng bên trái (Page 1 row 6 col 0, left triangle)
        "W.201a": (p1, 1552, 1724, 200, 278, None),
        # W.201b: Chỗ ngoặt nguy hiểm vòng bên phải (Page 1 row 6 col 0, right triangle)
        "W.201b": (p1, 1552, 1724, 278, 356, None),
        # W.205a: Đường giao nhau cùng mức (Page 1 row 0 col 0, first triangle)
        "W.205a": (p1, 444, 616, 220, 320, 0),
        # W.207a: Giao nhau với đường không ưu tiên (Page 1 row 0 col 1, first triangle)
        "W.207a": (p1, 444, 616, 360, 480, 0),
        # W.208: Giao nhau với đường ưu tiên (Page 1 row 0 col 2)
        "W.208": (p1, 444, 616, 671, 828, None),
        # W.224: Đường người đi bộ cắt ngang (Page 1 row 1 col 0)
        "W.224": (p1, 616, 789, 200, 356, None),
        # W.227: Công trường (Page 1 row 4 col 0)
        "W.227": (p1, 1136, 1329, 200, 356, None),
        # R.301a: Các xe chỉ được đi thẳng (Page 3 row 0 col 2)
        "R.301a": (p3, 297, 531, 521, 681, None),
        # R.301d: Các xe chỉ được rẽ phải (Page 3 row 0 col 3)
        "R.301d": (p3, 297, 531, 681, 843, None),
        # R.303: Nơi giao nhau chạy theo vòng xuyến (Page 3 row 0 col 1)
        "R.303": (p3, 297, 531, 360, 521, None),
        # I.401: Bắt đầu đường ưu tiên (Page 3 row 5 col 0)
        "I.401": (p3, 1322, 1563, 200, 360, None),
        # I.423a: Vị trí người đi bộ sang ngang (Page 4 row 0 col 1)
        "I.423a": (p4, 194, 387, 360, 521, None),
        # I.443: Chợ / Khu vực dịch vụ (Page 4 row 1 col 1)
        "I.443": (p4, 387, 740, 360, 521, None),
        # --- Các biển quan trọng mở rộng từ tài liệu ---
        # Biển cấm
        "P.101": (p2, 290, 483, 200, 354, None),  # Đường cấm
        "P.105": (p2, 483, 657, 200, 354, None),  # Cấm xe ô tô và xe máy
        "P.106a": (p2, 483, 657, 508, 663, None),  # Cấm ô tô tải
        "P.107a": (p2, 483, 657, 354, 508, None),  # Cấm ô tô khách
        "P.110a": (p2, 290, 483, 663, 817, None),  # Cấm xe đạp
        "P.111a": (p2, 290, 483, 817, 972, None),  # Cấm xe gắn máy
        "P.115": (p2, 1044, 1260, 972, 1126, None),  # Hạn chế chiều cao (3.5m)
        "P.116": (p2, 1044, 1260, 1126, 1280, None),  # Hạn chế chiều ngang (3.2m)
        "P.117": (p2, 1260, 1474, 200, 354, None),  # Hạn chế tải trọng toàn bộ (10t)
        "P.125": (p2, 1260, 1474, 972, 1126, None),  # Cấm vượt
        "P.126": (p2, 1260, 1474, 1126, 1280, None),  # Cấm ô tô tải vượt
        "P.128": (p2, 1474, 1647, 508, 663, None),  # Cấm sử dụng còi
        "P.131b": (p2, 1474, 1647, 972, 1126, None),  # Cấm đỗ xe ngày lẻ
        "P.131c": (p2, 1474, 1647, 1126, 1280, None),  # Cấm đỗ xe ngày chẵn
        "DP.135": (p2, 1647, 1882, 663, 817, None),  # Hết tất cả các lệnh cấm
        "DP.134": (p2, 1647, 1882, 972, 1126, None),  # Hết hạn chế tốc độ tối đa
        # Biển nguy hiểm
        "W.204": (p1, 616, 789, 513, 671, None),  # Đường hai chiều
        "W.209": (p1, 444, 616, 828, 985, None),  # Giao nhau có tín hiệu đèn
        "W.211a": (p1, 1724, 1918, 356, 513, None),  # Giao nhau với đường sắt có rào chắn
        "W.217": (p1, 789, 963, 200, 356, None),  # Cửa chui
        "W.218": (p1, 789, 963, 356, 513, None),  # Đường hầm
        "W.222a": (p1, 789, 963, 828, 985, None),  # Đường trơn
        "W.225": (p1, 616, 789, 356, 513, None),  # Trẻ em
        "W.226": (p1, 444, 616, 985, 1144, None),  # Đường người đi xe đạp cắt ngang
        # Biển hiệu lệnh & chỉ dẫn
        "R.122": (p3, 297, 531, 200, 360, None),  # Dừng lại (STOP)
        "R.301c": (p3, 297, 531, 843, 1004, None),  # Các xe chỉ được rẽ trái
        "R.305": (p3, 531, 705, 360, 521, None),  # Đường dành cho người đi bộ
        "R.306": (p3, 531, 705, 681, 843, None),  # Tốc độ tối thiểu cho phép
        "R.403a": (p3, 705, 898, 200, 360, None),  # Đường dành cho xe máy
        "R.403b": (p3, 705, 898, 360, 521, None),  # Đường dành cho ô tô con
        "R.420": (p3, 898, 1092, 521, 681, None),  # Bắt đầu khu đông dân cư
        "R.421": (p3, 898, 1092, 681, 843, None),  # Hết khu đông dân cư
        "I.402": (p3, 1322, 1563, 360, 521, None),  # Hết đoạn đường ưu tiên
        "I.407a": (p3, 1322, 1563, 681, 843, None),  # Đường một chiều
        "I.408": (p3, 1322, 1563, 843, 1004, None),  # Nơi đỗ xe (P)
        "I.409": (p3, 1322, 1563, 1165, 1325, None),  # Chỗ quay xe
        "I.436": (p4, 194, 387, 681, 843, None),  # Trạm CSGT
        "I.444": (p4, 194, 387, 843, 1004, None),  # Nơi đỗ xe cho người tàn tật
        "I.451": (p4, 740, 891, 681, 843, None),  # Bắt đầu đường cao tốc
        "I.452": (p4, 740, 891, 200, 360, None),  # Kết thúc đường cao tốc
        "S.501": (p4, 891, 1087, 521, 681, None),  # Phạm vi tác dụng
        "S.502": (p4, 891, 1087, 681, 843, None),  # Khoảng cách báo hiệu
    }

    cropped_counts = 0
    # Cắt và lưu từng ảnh
    for code, (page, y1, y2, x1, x2, sub_idx) in EXTRACTION_MAP.items():
        cell = page[y1:y2, x1:x2]
        crop = extract_sign_graphic(cell)
        if crop is not None:
            save_sign_images(code, crop)
            cropped_counts += 1
            logging.info("Đã cắt thành công: %s (%dx%d)", code, crop.shape[1], crop.shape[0])
        else:
            logging.warning("Không thể trích xuất đồ họa cho: %s", code)

    logging.info("Tổng số ảnh biển báo đã cắt thành công: %d", cropped_counts)

    # Cập nhật backend/data/signs_catalog.csv
    # Đọc danh sách hiện có
    existing_rows: list[dict[str, str]] = []
    if CATALOG_CSV_PATH.exists():
        with CATALOG_CSV_PATH.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing_rows = list(reader)

    # Cập nhật image_url cho các hàng hiện có (23 lớp đầu tiên)
    for row in existing_rows:
        code = row["sign_code"]
        img_path = FRONTEND_SIGNS_DIR / f"{code}.png"
        if img_path.exists():
            row["image_url"] = f"/signs/{code}.png"

    existing_codes = {r["sign_code"] for r in existing_rows}
    next_class_id = max(int(r["class_id"]) for r in existing_rows) + 1 if existing_rows else 23

    # Dữ liệu bổ sung từ he-thong-bien-bao.md
    ADDITIONAL_SIGNS = [
        # Biển cấm
        (
            "P.101",
            "Đường cấm",
            "Biển cấm",
            "Báo đường cấm tất cả các loại phương tiện (cơ giới và thô sơ) đi lại cả hai hướng, trừ các xe được ưu tiên theo quy định.",
            "Không điều khiển phương tiện đi vào tuyến đường có cắm biển này.",
            "high",
        ),
        (
            "P.105",
            "Cấm xe ô tô và xe máy",
            "Biển cấm",
            "Báo đường cấm tất cả các loại xe cơ giới và xe máy (mô tô) đi qua, trừ xe gắn máy và các xe được ưu tiên theo quy định.",
            "Người điều khiển ô tô và mô tô không đi vào đoạn đường này.",
            "high",
        ),
        (
            "P.106a",
            "Cấm ô tô tải",
            "Biển cấm",
            "Báo đường cấm tất cả các loại ô tô tải trừ các xe được ưu tiên theo quy định.",
            "Xe tải phải tìm lộ trình thay thế.",
            "high",
        ),
        (
            "P.107a",
            "Cấm xe ô tô khách",
            "Biển cấm",
            "Báo đường cấm ô tô chở khách đi qua trừ các xe ưu tiên.",
            "Ô tô chở khách không đi vào đường này.",
            "high",
        ),
        (
            "P.110a",
            "Cấm xe đạp",
            "Biển cấm",
            "Báo đường cấm xe đạp đi qua.",
            "Người đi xe đạp không đi vào đoạn đường này.",
            "medium",
        ),
        (
            "P.111a",
            "Cấm xe gắn máy",
            "Biển cấm",
            "Báo đường cấm xe gắn máy (dung tích xi lanh dưới 50cm3) đi qua.",
            "Không điều khiển xe gắn máy vào tuyến đường này.",
            "medium",
        ),
        (
            "P.115",
            "Hạn chế chiều cao (3.5m)",
            "Biển cấm",
            "Cấm các xe có chiều cao vượt quá 3.5m (tính cả hàng hóa) đi qua.",
            "Kiểm tra chiều cao xe trước khi qua gầm cầu/hầm.",
            "high",
        ),
        (
            "P.116",
            "Hạn chế chiều ngang xe (3.2m)",
            "Biển cấm",
            "Cấm các xe có chiều ngang vượt quá 3.2m đi qua đường hẹp.",
            "Kiểm tra khổ ngang thân xe và hàng hóa.",
            "high",
        ),
        (
            "P.117",
            "Hạn chế tải trọng toàn bộ xe (10t)",
            "Biển cấm",
            "Cấm các xe có tổng trọng lượng vượt quá 10 tấn đi qua.",
            "Xe quá tải trọng phải dừng lại hoặc đi tuyến đường khác.",
            "high",
        ),
        (
            "P.125",
            "Cấm vượt",
            "Biển cấm",
            "Cấm tất cả các loại xe cơ giới vượt nhau trên đoạn đường có cắm biển.",
            "Duy trì khoảng cách an toàn, tuyệt đối không lấn làn vượt xe.",
            "high",
        ),
        (
            "P.126",
            "Cấm ô tô tải vượt",
            "Biển cấm",
            "Cấm các loại ô tô tải vượt các xe cơ giới khác.",
            "Xe tải giữ làn đường, không thực hiện hành vi vượt.",
            "high",
        ),
        (
            "P.128",
            "Cấm sử dụng còi",
            "Biển cấm",
            "Báo cấm các loại xe sử dụng còi trong khu vực đặt biển (bệnh viện, trường học).",
            "Không bấm còi, hạn chế tiếng ồn.",
            "low",
        ),
        (
            "P.131b",
            "Cấm đỗ xe ngày lẻ",
            "Biển cấm",
            "Báo nơi cấm các loại xe đỗ vào các ngày lẻ trong tháng.",
            "Không đỗ xe vào ngày lẻ (1, 3, 5, 7, ...).",
            "medium",
        ),
        (
            "P.131c",
            "Cấm đỗ xe ngày chẵn",
            "Biển cấm",
            "Báo nơi cấm các loại xe đỗ vào các ngày chẵn trong tháng.",
            "Không đỗ xe vào ngày chẵn (2, 4, 6, 8, ...).",
            "medium",
        ),
        (
            "DP.135",
            "Hết tất cả các lệnh cấm",
            "Biển cấm",
            "Báo hiệu hết đoạn đường áp dụng tất cả các lệnh cấm trước đó.",
            "Tiếp tục hành trình theo quy tắc giao thông chung.",
            "info",
        ),
        (
            "DP.134",
            "Hết hạn chế tốc độ tối đa",
            "Biển cấm",
            "Báo hết đoạn đường bị hạn chế tốc độ tối đa quy định trước đó.",
            "Lưu thông theo tốc độ quy chuẩn của tuyến đường.",
            "info",
        ),
        # Biển nguy hiểm
        (
            "W.204",
            "Đường hai chiều",
            "Biển nguy hiểm và cảnh báo",
            "Báo trước đoạn đường phía trước lưu thông hai chiều.",
            "Đi đúng phần đường bên phải, quan sát xe ngược chiều.",
            "medium",
        ),
        (
            "W.209",
            "Giao nhau có tín hiệu đèn",
            "Biển nguy hiểm và cảnh báo",
            "Báo trước nơi giao nhau có đèn điều khiển giao thông.",
            "Giảm tốc độ và chuẩn bị chấp hành hiệu lệnh đèn.",
            "medium",
        ),
        (
            "W.211a",
            "Giao nhau với đường sắt có rào chắn",
            "Biển nguy hiểm và cảnh báo",
            "Báo trước sắp tới nơi đường bộ giao nhau với đường sắt có rào chắn.",
            "Giảm tốc độ, dừng lại trước rào chắn khi có tín hiệu đóng.",
            "high",
        ),
        (
            "W.217",
            "Cửa chui",
            "Biển nguy hiểm và cảnh báo",
            "Báo trước sắp đến cửa chui (hầm chui thấp).",
            "Chú ý chiều cao tĩnh không và giảm tốc độ.",
            "medium",
        ),
        (
            "W.218",
            "Đường hầm",
            "Biển nguy hiểm và cảnh báo",
            "Báo trước sắp vào đoạn đường hầm.",
            "Bật đèn chiếu gần, không vượt xe, giảm tốc độ.",
            "high",
        ),
        (
            "W.222a",
            "Đường trơn",
            "Biển nguy hiểm và cảnh báo",
            "Báo trước đoạn đường có độ ma sát thấp, dễ trơn trượt khi trời mưa.",
            "Giảm tốc độ, tránh phanh gấp hoặc đánh lái đột ngột.",
            "high",
        ),
        (
            "W.225",
            "Trẻ em",
            "Biển nguy hiểm và cảnh báo",
            "Báo trước gần đến khu vực trường học hoặc nơi thường có trẻ em qua lại.",
            "Giảm tốc độ tối đa, chú ý quan sát hai bên đường.",
            "high",
        ),
        (
            "W.226",
            "Đường người đi xe đạp cắt ngang",
            "Biển nguy hiểm và cảnh báo",
            "Báo trước nơi có người đi xe đạp thường xuyên cắt ngang đường.",
            "Quan sát và nhường đường cho xe đạp an toàn.",
            "medium",
        ),
        # Biển hiệu lệnh
        (
            "R.122",
            "Dừng lại (STOP)",
            "Biển hiệu lệnh",
            "Buộc tất cả các xe phải dừng lại trước vị trí đặt biển và chỉ được đi khi đường an toàn.",
            "Dừng hẳn xe lại quan sát an toàn mọi hướng trước khi đi tiếp.",
            "high",
        ),
        (
            "R.301c",
            "Các xe chỉ được rẽ trái",
            "Biển hiệu lệnh",
            "Các xe chỉ được phép rẽ trái ở nơi giao nhau.",
            "Bật xi nhan trái và thực hiện rẽ trái theo hiệu lệnh.",
            "medium",
        ),
        (
            "R.305",
            "Đường dành cho người đi bộ",
            "Biển hiệu lệnh",
            "Báo đường dành riêng cho người đi bộ, các loại xe không được đi vào.",
            "Phương tiện cơ giới và thô sơ không đi vào đường này.",
            "high",
        ),
        (
            "R.306",
            "Tốc độ tối thiểu cho phép (60km/h)",
            "Biển hiệu lệnh",
            "Bắt buộc các loại xe cơ giới phải chạy với tốc độ không nhỏ hơn trị số ghi trên biển.",
            "Duy trì tốc độ trên 60km/h (thường áp dụng trên cao tốc).",
            "medium",
        ),
        (
            "R.403a",
            "Đường dành cho xe máy",
            "Biển hiệu lệnh",
            "Báo hiệu bắt đầu làn đường dành riêng cho mô tô, xe máy.",
            "Xe máy đi vào làn đường này, ô tô không đi vào.",
            "medium",
        ),
        (
            "R.403b",
            "Đường dành cho ô tô con",
            "Biển hiệu lệnh",
            "Báo hiệu làn đường dành riêng cho ô tô con.",
            "Ô tô con lưu thông đúng làn chỉ định.",
            "medium",
        ),
        (
            "R.420",
            "Bắt đầu khu đông dân cư",
            "Biển hiệu lệnh",
            "Báo hiệu bắt đầu đoạn đường qua khu đông dân cư, áp dụng tốc độ nội thị.",
            "Giảm tốc độ theo quy chuẩn khu đông dân cư (50km/h hoặc 60km/h).",
            "high",
        ),
        (
            "R.421",
            "Hết khu đông dân cư",
            "Biển hiệu lệnh",
            "Báo hiệu hết đoạn đường qua khu đông dân cư.",
            "Lưu thông theo quy chuẩn tốc độ ngoài đô thị.",
            "info",
        ),
        # Biển chỉ dẫn
        (
            "I.402",
            "Hết đoạn đường ưu tiên",
            "Biển chỉ dẫn",
            "Báo hiệu hết đoạn đường được quyền ưu tiên.",
            "Giảm tốc độ và nhường đường theo quy tắc giao thông chung.",
            "info",
        ),
        (
            "I.407a",
            "Đường một chiều",
            "Biển chỉ dẫn",
            "Chỉ dẫn phía trước là đường một chiều.",
            "Chỉ đi theo một chiều mũi tên, không quay đầu hoặc lùi xe.",
            "medium",
        ),
        (
            "I.408",
            "Nơi đỗ xe (P)",
            "Biển chỉ dẫn",
            "Chỉ dẫn vị trí được phép dừng đỗ xe.",
            "Đỗ xe ngay ngắn đúng vạch quy định.",
            "info",
        ),
        (
            "I.409",
            "Chỗ quay xe",
            "Biển chỉ dẫn",
            "Chỉ dẫn vị trí được phép quay đầu xe.",
            "Bật đèn tín hiệu và quay đầu xe tại điểm mở dải phân cách.",
            "info",
        ),
        (
            "I.436",
            "Trạm cảnh sát giao thông",
            "Biển chỉ dẫn",
            "Chỉ dẫn vị trí đặt trạm kiểm soát của cảnh sát giao thông.",
            "Giảm tốc độ và chuẩn bị xuất trình giấy tờ khi có hiệu lệnh.",
            "info",
        ),
        (
            "I.444",
            "Nơi đỗ xe cho người tàn tật",
            "Biển chỉ dẫn",
            "Chỉ dẫn vị trí đỗ xe dành riêng cho người khuyết tật.",
            "Không chiếm dụng vị trí đỗ xe ưu tiên này.",
            "info",
        ),
        (
            "I.451",
            "Bắt đầu đường cao tốc",
            "Biển chỉ dẫn",
            "Chỉ dẫn bắt đầu tuyến đường cao tốc.",
            "Tuân thủ nghiêm ngặt quy tắc tốc độ và làn đường cao tốc.",
            "high",
        ),
        (
            "I.452",
            "Kết thúc đường cao tốc",
            "Biển chỉ dẫn",
            "Chỉ dẫn kết thúc tuyến đường cao tốc.",
            "Giảm tốc độ và nhập làn vào đường thông thường an toàn.",
            "medium",
        ),
        # Biển phụ
        (
            "S.501",
            "Phạm vi tác dụng của biển",
            "Biển phụ",
            "Chỉ dẫn chiều dài đoạn đường chịu tác dụng của biển báo chính.",
            "Tuân thủ biển chính trong suốt cự ly ghi trên biển phụ.",
            "info",
        ),
        (
            "S.502",
            "Khoảng cách đến đối tượng báo hiệu",
            "Biển phụ",
            "Chỉ dẫn cự ly từ vị trí đặt biển đến vị trí bắt đầu hiệu lực.",
            "Chuẩn bị trước thao tác lái xe theo khoảng cách ghi.",
            "info",
        ),
    ]

    for code, name, group, meaning, action, warn in ADDITIONAL_SIGNS:
        if code not in existing_codes:
            img_url = f"/signs/{code}.png" if (FRONTEND_SIGNS_DIR / f"{code}.png").exists() else ""
            existing_rows.append(
                {
                    "class_id": str(next_class_id),
                    "sign_code": code,
                    "name": name,
                    "group_name": group,
                    "meaning": meaning,
                    "recommended_action": action,
                    "warning_level": warn,
                    "image_url": img_url,
                    "legal_source": "QCVN 41:2019/BGTVT",
                    "source_checked_at": "2026-10-31",
                }
            )
            next_class_id += 1

    # Ghi lại file CSV
    fieldnames = [
        "class_id",
        "sign_code",
        "name",
        "group_name",
        "meaning",
        "recommended_action",
        "warning_level",
        "image_url",
        "legal_source",
        "source_checked_at",
    ]
    with CATALOG_CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_rows)

    logging.info("Đã cập nhật file %s với tổng cộng %d biển báo.", CATALOG_CSV_PATH, len(existing_rows))


if __name__ == "__main__":
    main()
