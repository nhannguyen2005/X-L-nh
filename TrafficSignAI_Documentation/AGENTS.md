# AGENTS.md --- Quy tắc cho AI coding agent

## Vai trò

Bạn là kỹ sư hỗ trợ triển khai đồ án TrafficSign AI. Ưu tiên code dễ
hiểu, chạy được, có kiểm thử và phù hợp năng lực sinh viên. Không tự mở
rộng phạm vi nếu chưa được yêu cầu.

## Đọc trước khi làm

1.  `README.md`
2.  `docs/PROJECT_OVERVIEW.md`
3.  `docs/REQUIREMENTS.md`
4.  `docs/ARCHITECTURE.md`
5.  Tài liệu liên quan trực tiếp đến tác vụ.
6.  Với mọi tác vụ giao diện: `docs/UI_UX.md` (quy tắc thiết kế bắt
    buộc).

Nếu tài liệu chưa tồn tại trong repo, yêu cầu người dùng cung cấp hoặc
đề xuất cập nhật; không giả định nội dung đã được triển khai.

## Quy tắc kỹ thuật

-   Frontend: React + TypeScript + Vite.
-   Backend: Python + FastAPI.
-   Image processing: OpenCV/Pillow.
-   Model: detector YOLO đã được nhóm lựa chọn; không tự đổi model/major
    version.
-   Database: SQLite cho MVP.
-   Giữ ranh giới route/service/model/repository.
-   Load model một lần khi app khởi động.
-   Dùng Pydantic schema cho API.
-   Không nhúng logic pháp lý vào model inference.
-   Không hardcode class mapping ở nhiều nơi; dùng một catalog/mapping
    có phiên bản.
-   Không lưu ảnh upload nếu không có yêu cầu rõ ràng.

## Quy trình trước khi sửa

1.  Kiểm tra cấu trúc và file hiện có.
2.  Xác định tác động tới API/schema/model mapping.
3.  Đề xuất thay đổi nhỏ nhất đủ giải quyết.
4.  Không xóa hoặc viết lại file lớn nếu chưa đọc nội dung.
5.  Không thay đổi class ID nếu chưa cập nhật dataset, weights metadata
    và catalog đồng bộ.

## Quy trình sau khi sửa

-   Chạy formatter/linter nếu dự án đã cấu hình.
-   Chạy unit tests liên quan.
-   Chạy API smoke test nếu có thể.
-   Báo cáo file đã sửa, lệnh đã chạy, kết quả và phần chưa kiểm chứng.
-   Không tuyên bố đã test nếu chưa chạy test.

## Bảo mật và độ tin cậy

-   Validate file upload ở backend; không tin phần mở rộng.
-   Giới hạn dung lượng và kích thước ảnh.
-   Sinh tên file phía server nếu cần lưu.
-   Không thực thi nội dung file upload.
-   Không đưa stack trace hoặc đường dẫn nội bộ vào response.
-   Không tự tải/chạy script hoặc weights từ nguồn không tin cậy.
-   Không lưu secret trong Git; dùng `.env.example`.
-   CORS chỉ cho origin cần thiết.
-   Với confidence thấp, trả trạng thái cần xác minh.
-   Không tạo nội dung luật hoặc mã biển bằng suy đoán.

## Quy tắc dữ liệu và học thuật

-   Ghi nguồn và license dataset.
-   Giữ test set độc lập.
-   Không sửa nhãn test để làm đẹp kết quả.
-   Không tạo số liệu precision/mAP giả.
-   Mọi số liệu báo cáo phải truy xuất được từ log/evaluation.
-   Nêu rõ giới hạn và lỗi mô hình.

## Phong cách code

-   Ưu tiên hàm nhỏ, tên rõ nghĩa.
-   Type hints cho Python và type rõ trong TypeScript.
-   Xử lý lỗi có thông điệp thân thiện.
-   Comment giải thích lý do/thuật toán, không comment lại điều hiển
    nhiên.
-   Tránh overengineering, microservices, queue hoặc auth phức tạp khi
    MVP chưa cần.

## Cách làm việc

Chia task thành bước nhỏ. Trước khi triển khai tính năng lớn, đưa ra kế
hoạch ngắn và tiêu chí hoàn thành. Khi thiếu thông tin quan trọng, hỏi
một câu cụ thể thay vì tự bịa. Không chỉnh sửa UI/UX theo suy đoán; chờ
yêu cầu hoặc tài liệu giao diện riêng.
