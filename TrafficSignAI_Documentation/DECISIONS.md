# 13. Nhật ký quyết định kỹ thuật

Ghi ngày, quyết định, lựa chọn thay thế và lý do. Các quyết định dưới
đây là mặc định đề xuất, có thể cập nhật khi nhóm thử nghiệm.

## D-001 --- Chọn object detection

**Quyết định:** dùng object detection cho ảnh đường phố.

**Lý do:** cần tìm cả vị trí và loại biển trong ảnh có nền phức
tạp/nhiều đối tượng. Classification chỉ phân lớp ảnh đã crop sẵn.

## D-002 --- React + FastAPI

**Quyết định:** frontend React/TypeScript, backend FastAPI.

**Lý do:** tách giao diện khỏi pipeline Python/OpenCV/model; FastAPI hỗ
trợ schema và tài liệu API tự động.

## D-003 --- SQLite cho MVP

**Quyết định:** SQLite.

**Lý do:** dễ cài đặt, đủ cho ứng dụng demo cá nhân/nhóm nhỏ. Không cần
vận hành database server riêng.

## D-004 --- Detector nhỏ

**Quyết định:** bắt đầu bằng biến thể YOLO nano.

**Lý do:** cân bằng giữa độ phức tạp triển khai và tốc độ thử nghiệm.
Phải kiểm tra license và đo thực tế.

## D-005 --- Giới hạn lớp

**Quyết định:** chọn 10--20 lớp tùy dataset.

**Lý do:** ưu tiên dữ liệu đủ chất lượng và đánh giá sâu hơn là mở rộng
lớp nhưng thiếu mẫu.

## D-006 --- Cảnh báo dựa trên catalog

**Quyết định:** model chỉ dự đoán class; nội dung ý nghĩa/cảnh báo lấy
từ catalog đã kiểm chứng.

**Lý do:** tránh để mô hình sinh văn bản pháp lý không đáng tin. Cần lưu
nguồn và ngày kiểm tra.

## D-007 --- Không lưu ảnh gốc mặc định

**Quyết định:** xử lý trong bộ nhớ, chỉ lưu metadata tối thiểu nếu bật
history.

**Lý do:** giảm rủi ro riêng tư và giảm dung lượng lưu trữ.
