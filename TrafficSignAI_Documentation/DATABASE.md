# 8. Thiết kế cơ sở dữ liệu

## 8.1. Lựa chọn

SQLite phù hợp đồ án chạy local, không cần server database riêng. Dùng
SQLAlchemy hoặc SQLModel để thao tác. Nếu chỉ cần catalog tĩnh, có thể
bắt đầu bằng JSON/CSV có kiểm soát phiên bản; lịch sử quét mới cần
database.

## 8.2. Bảng `traffic_signs`

  Cột                  Kiểu             Ý nghĩa
  -------------------- ---------------- -------------------------------
  id                   INTEGER PK       ID nội bộ
  class_id             INTEGER UNIQUE   ID lớp trong model
  sign_code            TEXT UNIQUE      Mã biển đã xác minh
  name                 TEXT             Tên biển
  group_name           TEXT             Nhóm biển
  meaning              TEXT             Ý nghĩa
  recommended_action   TEXT             Khuyến nghị hành vi
  warning_level        TEXT             low/medium/high/info
  image_url            TEXT nullable    Ảnh minh họa có quyền sử dụng
  legal_source         TEXT             Nguồn văn bản/tài liệu
  source_checked_at    DATE             Ngày kiểm tra nguồn
  updated_at           DATETIME         Ngày cập nhật

## 8.3. Bảng `scan_history` (tùy chọn)

  Cột                 Kiểu          Ý nghĩa
  ------------------- ------------- ------------------------------------------
  id                  INTEGER PK    ID lịch sử
  request_id          TEXT UNIQUE   Mã yêu cầu
  original_filename   TEXT          Tên file đã làm sạch
  created_at          DATETIME      Thời điểm quét
  detection_count     INTEGER       Số biển phát hiện
  processing_ms       REAL          Thời gian xử lý
  result_json         TEXT          Kết quả tối giản, không lưu dữ liệu thừa

Không lưu ảnh gốc mặc định. Nếu cần lưu ảnh kết quả để demo, cần giới
hạn dung lượng và có chính sách xóa.

## 8.4. Ràng buộc

-   `class_id` phải khớp mapping model.
-   `warning_level` chỉ nhận các giá trị được định nghĩa.
-   `sign_code` không trùng.
-   Nội dung `legal_source` không được để trống với bản ghi có diễn giải
    pháp lý.
-   Khi cập nhật class mapping, phải cập nhật đồng thời model metadata
    và catalog.

## 8.5. Dữ liệu mẫu

Chỉ tạo dữ liệu mẫu sau khi xác minh mã biển, tên gọi và nội dung từ
nguồn đáng tin cậy. Không lấy tên lớp tự đặt làm mã biển pháp lý. Lưu
nguồn và ngày kiểm tra cho từng bản ghi.

## 8.6. Migration và seed

-   Có script `seed_signs.py` đọc CSV/JSON đã review.
-   Có script tạo database.
-   Seed chạy nhiều lần không tạo bản ghi trùng (upsert theo `class_id`
    hoặc `sign_code`).
-   Nếu thay đổi schema, dùng migration hoặc ghi rõ cách tạo lại
    database cho đồ án.
