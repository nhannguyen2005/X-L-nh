# TrafficSign AI --- Tài liệu dự án

> Webapp nhận diện biển báo giao thông Việt Nam và giải thích ý
> nghĩa/cảnh báo bằng xử lý ảnh và học sâu.

## Mục tiêu

Xây dựng ứng dụng web cho phép người dùng tải ảnh hoặc chụp ảnh có biển
báo; hệ thống phát hiện và phân loại biển báo, tra cứu thông tin tương
ứng, sau đó hiển thị giải thích và khuyến nghị hành vi an toàn.

## Bộ tài liệu

  -----------------------------------------------------------------------
  Tệp                                 Nội dung
  ----------------------------------- -----------------------------------
  `PROJECT_OVERVIEW.md`               Bài toán, mục tiêu, phạm vi, đóng
                                      góp

  `REQUIREMENTS.md`                   Yêu cầu chức năng/phi chức năng,
                                      tiêu chí nghiệm thu

  `ARCHITECTURE.md`                   Kiến trúc tổng thể và luồng dữ liệu

  `IMAGE_PROCESSING.md`               Quy trình xử lý ảnh và cơ sở lý
                                      thuyết

  `DATASET.md`                        Thu thập, gán nhãn, chia tập dữ
                                      liệu

  `MODEL_TRAINING.md`                 Huấn luyện, cấu hình, lưu mô hình

  `API_SPEC.md`                       Hợp đồng API giữa frontend và
                                      backend

  `DATABASE.md`                       Thiết kế dữ liệu biển báo và lịch
                                      sử

  `TESTING_EVALUATION.md`             Kiểm thử chức năng và đánh giá mô
                                      hình

  `MILESTONES.md`                     Kế hoạch triển khai theo tuần

  `REPORT_GUIDE.md`                   Dàn ý báo cáo và nội dung cần chứng
                                      minh

  `DEMO_CHECKLIST.md`                 Kịch bản demo và kiểm tra trước bảo
                                      vệ

  `AGENTS.md`                         Quy tắc làm việc cho AI coding
                                      agent

  `DECISIONS.md`                      Các quyết định kỹ thuật và lý do

  `UI_UX.md`                          Quy tắc thiết kế giao diện và trải
                                      nghiệm người dùng
  -----------------------------------------------------------------------

## Công nghệ đề xuất

-   Frontend: React + TypeScript + Vite.
-   Backend: Python + FastAPI.
-   Xử lý ảnh: OpenCV + Pillow.
-   Mô hình: YOLO phiên bản nhỏ (ví dụ YOLOv8n hoặc phiên bản
    Ultralytics tương thích môi trường), fine-tune trên bộ dữ liệu biển
    báo đã kiểm tra giấy phép.
-   Lưu trữ: SQLite cho đồ án cá nhân; có thể chuyển PostgreSQL nếu cần.
-   Kiểm thử: pytest, kiểm thử API, kiểm thử thủ công giao diện.

Phiên bản thư viện thực tế phải được khóa trong
`requirements.txt`/lockfile sau khi kiểm tra tương thích. Không ghi
trong báo cáo rằng mô hình đã đạt một độ chính xác cụ thể nếu chưa đo
trên tập test độc lập.

## Cách bắt đầu

1.  Đọc `PROJECT_OVERVIEW.md` và chốt phạm vi với giảng viên.
2.  Đọc `DATASET.md`; xác định bộ dữ liệu và quyền sử dụng.
3.  Xây pipeline nhận diện độc lập trước, sau đó mới tích hợp web.
4.  Làm theo `MILESTONES.md`; mỗi mốc phải có đầu ra kiểm chứng được.
5.  Hoàn thiện báo cáo theo `REPORT_GUIDE.md`.

## Nguyên tắc học thuật

-   Ghi rõ nguồn dữ liệu, giấy phép, nguồn tham khảo và phiên bản mô
    hình.
-   Phân biệt kết quả thực nghiệm với mục tiêu kỳ vọng.
-   Không dùng ảnh trong tập train để báo cáo kết quả test.
-   Không tuyên bố hệ thống nhận diện chính xác trong mọi điều kiện thực
    tế.
-   Mọi cảnh báo pháp lý phải được đối chiếu văn bản pháp luật hiện hành
    và ghi ngày kiểm tra.
