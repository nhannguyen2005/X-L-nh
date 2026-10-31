# 10. Kế hoạch triển khai

Kế hoạch mẫu 6 tuần; điều chỉnh theo lịch môn học và quy mô nhóm.

## Tuần 1 --- Chốt bài toán và khảo sát

**Việc làm** - Chốt tên đề tài, mục tiêu, phạm vi lớp. - Khảo sát
dataset, giấy phép và tài liệu pháp lý. - Tạo repository, cấu trúc thư
mục, môi trường. - Viết mô tả bài toán và tiêu chí nghiệm thu.

**Đầu ra:** danh sách lớp dự kiến, nguồn dataset, sơ đồ kiến trúc,
backlog.

**Điều kiện qua mốc:** có dữ liệu hợp lệ để thử nghiệm hoặc kế hoạch tự
thu thập khả thi.

## Tuần 2 --- Dataset và baseline

**Việc làm** - Chuẩn hóa nhãn. - Chia train/val/test. - Kiểm tra class
distribution, box và ảnh lỗi. - Huấn luyện baseline. - Lưu kết quả và
ảnh dự đoán.

**Đầu ra:** dataset card, script kiểm tra, checkpoint baseline, metrics
ban đầu.

**Điều kiện qua mốc:** pipeline train/evaluate chạy tái lập.

## Tuần 3 --- Cải thiện và đánh giá mô hình

**Việc làm** - Phân tích false positive/false negative. - Thử điều chỉnh
augmentation/threshold. - Đánh giá theo lớp và điều kiện ảnh. - Chốt
checkpoint.

**Đầu ra:** mô hình được chọn, bảng metrics, bộ ảnh lỗi.

**Điều kiện qua mốc:** có test độc lập và giải thích được giới hạn.

## Tuần 4 --- Backend

**Việc làm** - Tạo FastAPI. - Tích hợp model load-once. - Xây API
detection, signs, health. - Xây catalog và SQLite/history nếu đủ thời
gian. - Viết test API.

**Đầu ra:** API chạy độc lập, OpenAPI docs, JSON response đúng schema.

## Tuần 5 --- Frontend và tích hợp

**Việc làm** - Upload ảnh và hiển thị trạng thái. - Hiển thị ảnh kết
quả, box, confidence và nội dung biển. - Xử lý không phát hiện/lỗi. -
Tích hợp camera nếu MVP đã ổn. - Kiểm thử end-to-end.

**Đầu ra:** webapp chạy xuyên suốt từ ảnh đến cảnh báo.

## Tuần 6 --- Hoàn thiện và bảo vệ

**Việc làm** - Chạy test hồi quy. - Đo latency trên máy demo. - Chụp ảnh
màn hình, chuẩn bị ảnh demo. - Hoàn thiện báo cáo, slide, video dự
phòng. - Tổng duyệt kịch bản.

**Đầu ra:** mã nguồn, hướng dẫn cài đặt, báo cáo, slide, demo.

## Ưu tiên khi thiếu thời gian

1.  Model nhận diện chạy ổn định.
2.  API nhận ảnh và trả kết quả đúng.
3.  Frontend upload và hiển thị kết quả.
4.  Catalog giải thích biển báo.
5.  Đánh giá mô hình và báo cáo trung thực.
6.  Lịch sử, camera, tài khoản là phần mở rộng.

Không hy sinh đánh giá khoa học để thêm nhiều chức năng phụ.
