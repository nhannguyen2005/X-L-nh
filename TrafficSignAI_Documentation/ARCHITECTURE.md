# 3. Kiến trúc hệ thống

## 3.1. Kiến trúc đề xuất

Frontend React/TypeScript gọi FastAPI. Backend xác thực ảnh, xử lý ảnh,
gọi model inference, ánh xạ class sang dữ liệu biển báo, tạo ảnh kết quả
và trả JSON. SQLite lưu lịch sử và dữ liệu nội dung ở quy mô đồ án.

``` text
[Browser: React]
   | multipart/form-data
   v
[FastAPI: /api/v1/detections]
   |
   +--> Image validation
   |
   +--> OpenCV preprocessing
   |
   +--> Detector inference (YOLO)
   |
   +--> Post-processing / coordinate mapping
   |
   +--> Sign catalog lookup
   |
   +--> Result image renderer
   |
   +--> SQLite history (optional)
   v
[JSON response + annotated image URL/base64]
```

## 3.2. Nguyên tắc phân lớp backend

-   `api/`: route và schema HTTP, không chứa thuật toán model.
-   `core/`: cấu hình, logging, giới hạn upload.
-   `services/`: use-case xử lý ảnh và nhận diện.
-   `ml/`: load model, inference, chuyển đổi kết quả.
-   `repositories/`: truy vấn database.
-   `models/`: ORM entities.
-   `schemas/`: Pydantic request/response.
-   `data/`: catalog có kiểm soát phiên bản.
-   `tests/`: unit, integration và API tests.

## 3.3. Cấu trúc thư mục tham khảo

``` text
traffic-sign-ai/
├── README.md
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   ├── IMAGE_PROCESSING.md
│   ├── DATASET.md
│   ├── MODEL_TRAINING.md
│   ├── API_SPEC.md
│   ├── DATABASE.md
│   ├── TESTING_EVALUATION.md
│   ├── MILESTONES.md
│   ├── REPORT_GUIDE.md
│   ├── DEMO_CHECKLIST.md
│   └── DECISIONS.md
├── frontend/
│   └── src/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── ml/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── weights/
│   └── requirements.txt
├── dataset/
│   ├── raw/             # không commit dữ liệu lớn nếu chưa rõ license
│   ├── processed/
│   └── data.yaml
├── training/
│   ├── train.py
│   └── evaluate.py
└── artifacts/
    ├── metrics/
    └── samples/
```

## 3.4. Luồng xử lý một yêu cầu

1.  Frontend chọn ảnh và kiểm tra sơ bộ định dạng/kích thước.
2.  Gửi `POST /api/v1/detections` dạng multipart.
3.  Backend kiểm tra phần mở rộng, MIME, magic bytes, dung lượng và khả
    năng giải mã.
4.  Chuẩn hóa ảnh; giữ kích thước gốc để quy đổi tọa độ.
5.  Model suy luận; hậu xử lý box và confidence.
6.  Ánh xạ class ID sang catalog; class không có catalog phải được đánh
    dấu unknown.
7.  Vẽ box trên bản sao ảnh; không ghi đè ảnh gốc.
8.  Trả detections, metadata và đường dẫn ảnh kết quả hoặc ảnh base64.
9.  Ghi lịch sử nếu được bật và có chính sách lưu trữ rõ ràng.

## 3.5. Quản lý model

-   Load model một lần khi ứng dụng khởi động, không load lại ở mỗi
    request.
-   Kiểm tra file weights tồn tại; nếu không có, báo lỗi cấu hình rõ
    ràng.
-   Có cấu hình `MODEL_PATH`, `CONFIDENCE_THRESHOLD`, `IOU_THRESHOLD`,
    `IMAGE_SIZE`, `DEVICE`.
-   Ghi phiên bản model và dataset trong metadata.
-   Không tự tải weights từ URL không tin cậy khi server khởi động.

## 3.6. Triển khai

MVP chạy local: - Frontend dev server riêng. - FastAPI chạy bằng
Uvicorn. - SQLite lưu cục bộ. - Model chạy CPU trước; GPU chỉ bật nếu
môi trường hỗ trợ.

Khi demo, chạy cả frontend và backend trên cùng máy. Ghi rõ yêu cầu RAM,
dung lượng model và thời gian khởi động thực tế.
