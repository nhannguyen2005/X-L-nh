# 6. Huấn luyện mô hình

## 6.1. Lựa chọn mô hình

Đề xuất bắt đầu bằng một detector YOLO phiên bản nhỏ (ví dụ YOLOv8n) vì
dễ fine-tune, suy luận tương đối nhanh và có hệ sinh thái công cụ. Kiểm
tra giấy phép framework/weights trước khi sử dụng trong sản phẩm hoặc
phân phối. Không mặc định phiên bản mới nhất là tốt nhất; chọn phiên bản
ổn định, tương thích Python, PyTorch và máy tính.

So sánh tùy khả năng: - Baseline: model pretrained fine-tune trên
dataset. - Lightweight: biến thể nano/small. - Nếu thời gian cho phép:
so sánh với một baseline khác.

## 6.2. Môi trường

Tạo môi trường ảo Python riêng. Cài phiên bản package tương thích theo
tài liệu framework và phần cứng. Ghi lại: - Python version. - PyTorch
version. - Ultralytics/framework version. - OpenCV version. - CUDA/cuDNN
nếu dùng GPU. - Hệ điều hành và GPU.

Không ghi cứng lệnh CUDA chung cho mọi máy; chọn đúng build theo môi
trường. Có thể huấn luyện CPU để kiểm thử pipeline nhưng thời gian sẽ
dài.

## 6.3. Cấu hình thí nghiệm ban đầu

Thông số khởi điểm cần điều chỉnh bằng validation: - Model: nano. -
Image size: 640. - Epoch: 50--100 tùy dataset và thời gian. - Batch: phù
hợp VRAM/RAM. - Optimizer và learning rate: dùng mặc định có kiểm soát
trước, sau đó mới tinh chỉnh. - Early stopping/patience nếu framework hỗ
trợ. - Seed cố định để tăng khả năng tái lập.

Đây là cấu hình khởi điểm, không phải bảo đảm kết quả.

## 6.4. Quy trình

1.  Kiểm tra dataset và file YAML.
2.  Chạy một epoch hoặc một batch để xác nhận dữ liệu đọc đúng.
3.  Huấn luyện baseline.
4.  Theo dõi loss train/validation, precision, recall, mAP50, mAP50-95.
5.  Chọn checkpoint theo validation, không chọn theo test.
6.  Đánh giá checkpoint cuối cùng trên test độc lập.
7.  Chạy inference trên ảnh thực tế ngoài dataset.
8.  Lưu weights, config, log và kết quả mẫu.

## 6.5. Đầu ra cần lưu

``` text
artifacts/
├── weights/
│   └── best.pt
├── metrics/
│   ├── results.csv
│   ├── confusion_matrix.png
│   ├── PR_curve.png
│   └── evaluation.json
├── config/
│   └── experiment.yaml
└── samples/
    ├── input/
    └── output/
```

Không commit dataset/weights lớn vào Git nếu không cần; dùng Git LFS
hoặc lưu trữ riêng theo quy định môn học.

## 6.6. Tích hợp inference

Tạo lớp `Detector`: - Khởi tạo model một lần. - Hàm `predict(image)`
nhận ảnh đã giải mã. - Trả danh sách detection chuẩn hóa: `class_id`,
`class_name`, `confidence`, `x1`, `y1`, `x2`, `y2`. - Tọa độ phải thuộc
ảnh gốc. - Có thể cấu hình threshold. - Không để logic HTTP hoặc
database trong lớp model.

## 6.7. Ngưỡng và hiệu chỉnh

Chọn confidence threshold dựa trên validation. Có thể báo cáo
precision-recall theo nhiều ngưỡng. Không chọn threshold trên test rồi
công bố kết quả test như đánh giá độc lập.

## 6.8. Kiểm tra lỗi thường gặp

-   Sai mapping class ID giữa YAML và catalog.
-   Nhãn YOLO chưa chuẩn hóa.
-   Box lệch do quên bỏ padding letterbox.
-   Model load mỗi request gây chậm.
-   Ảnh BGR/RGB không thống nhất.
-   Dataset leakage.
-   Model dự đoán tốt trên ảnh train nhưng kém trên ảnh mới.
-   Checkpoint và config không cùng phiên bản.
