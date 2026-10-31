# TrafficSign AI - Model Weights

Thư mục lưu trữ trọng số mô hình object detection (YOLOv8n hoặc tương đương).

## Quy ước
- Tệp mặc định: `best.pt` (hoặc cấu hình đường dẫn qua biến môi trường `MODEL_PATH` trong `.env`).
- Khi khởi động ứng dụng backend, `TrafficSignDetector` sẽ nạp trọng số từ tệp này một lần duy nhất (`load-once pattern`).
- Nếu chưa có file `best.pt`, API `/health` sẽ trả `model_loaded: false` và endpoint `/detections` sẽ trả mã lỗi `503 MODEL_NOT_READY`.
