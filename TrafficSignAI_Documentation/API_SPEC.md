# 7. Đặc tả API

Base URL local: `http://localhost:8000/api/v1`

## 7.1. POST `/detections`

Nhận một ảnh và trả kết quả nhận diện.

**Request:** `multipart/form-data` - `file`: ảnh JPG/JPEG/PNG. -
`confidence` (optional): ngưỡng confidence hợp lệ trong khoảng 0--1;
server áp giới hạn cho phép. - `save_history` (optional): boolean, mặc
định false hoặc theo cấu hình.

**Response 200:**

``` json
{
  "request_id": "uuid",
  "status": "completed",
  "image": {
    "width": 1280,
    "height": 720,
    "annotated_image": "/api/v1/detections/uuid/image"
  },
  "summary": {
    "detection_count": 1,
    "processing_ms": 184.2
  },
  "detections": [
    {
      "class_id": 0,
      "class_name": "cam_di_nguoc_chieu",
      "confidence": 0.93,
      "bbox": {"x1": 100, "y1": 80, "x2": 240, "y2": 220},
      "sign": {
        "sign_code": "CODE_FROM_VERIFIED_SOURCE",
        "name": "Tên biển báo đã xác minh",
        "group": "Biển cấm",
        "meaning": "Mô tả ý nghĩa",
        "recommended_action": "Hành vi cần tuân thủ",
        "warning_level": "high",
        "source": "Nguồn tham khảo"
      },
      "verification_required": false
    }
  ],
  "warnings": []
}
```

Ví dụ trên chỉ minh họa cấu trúc; nội dung class và mã biển phải lấy từ
catalog đã kiểm chứng.

## 7.2. GET `/signs`

Query params: - `q`: tìm theo tên/mã. - `group`: nhóm biển. - `page`,
`page_size`: phân trang.

Trả danh sách bản ghi biển báo và metadata.

## 7.3. GET `/signs/{sign_id}`

Trả thông tin chi tiết một biển báo.

## 7.4. GET `/history`

Trả lịch sử quét nếu tính năng được bật. Nên giới hạn số bản ghi và phân
trang.

## 7.5. GET `/health`

Trả trạng thái backend và model:

``` json
{
  "status": "ok",
  "model_loaded": true,
  "model_version": "experiment-version"
}
```

Không trả đường dẫn nội bộ hoặc thông tin nhạy cảm.

## 7.6. Mã lỗi

  HTTP   Code                     Ý nghĩa
  ------ ------------------------ -------------------------
  400    INVALID_IMAGE            File không giải mã được
  413    FILE_TOO_LARGE           Ảnh vượt giới hạn
  415    UNSUPPORTED_MEDIA_TYPE   Định dạng không hỗ trợ
  422    INVALID_PARAMETER        Tham số không hợp lệ
  500    INFERENCE_ERROR          Lỗi suy luận
  503    MODEL_NOT_READY          Model chưa sẵn sàng

Lỗi có cấu trúc:

``` json
{
  "error": {
    "code": "INVALID_IMAGE",
    "message": "Không thể đọc ảnh được tải lên."
  },
  "request_id": "uuid"
}
```

## 7.7. Quy ước

-   Dùng Pydantic response schema; không trả trực tiếp object framework.
-   Tọa độ box là pixel trên ảnh gốc, quy ước x1/y1 góc trái trên, x2/y2
    góc phải dưới.
-   Confidence là số thực 0--1.
-   Thời gian xử lý tính bằng millisecond và ghi rõ phạm vi đo.
-   Không trả stack trace cho client.
-   CORS chỉ cho phép origin frontend đã cấu hình.
-   Giới hạn file upload ở backend; kiểm tra MIME không chỉ dựa vào tên
    file.
