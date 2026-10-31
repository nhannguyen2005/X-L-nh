# 1. Tổng quan đề tài

## 1.1. Tên đề tài đề xuất

**Xây dựng hệ thống web nhận diện biển báo giao thông Việt Nam và hỗ trợ
cảnh báo bằng kỹ thuật xử lý ảnh.**

Tên tiếng Anh: **Vietnamese Traffic Sign Recognition and Warning Web
Application**.

## 1.2. Bối cảnh và lý do chọn đề tài

Biển báo giao thông truyền tải các quy định, hướng dẫn và cảnh báo trên
đường. Việc nhận biết đúng biển báo có ý nghĩa đối với an toàn giao
thông. Với ảnh chụp trong thực tế, biển báo có thể nhỏ, nghiêng, mờ,
thiếu sáng, bị che khuất hoặc xuất hiện cùng nhiều vật thể khác. Đây là
bài toán phù hợp để vận dụng xử lý ảnh, phát hiện đối tượng và phân loại
hình ảnh.

Đồ án xây dựng một ứng dụng web minh họa quy trình từ ảnh đầu vào đến
kết quả nhận diện và thông tin giải thích. Hệ thống hướng đến mục đích
học tập, không điều khiển phương tiện và không thay thế việc quan sát
biển báo thực tế.

## 1.3. Phát biểu bài toán

**Đầu vào:** một ảnh tĩnh có thể chứa một hoặc nhiều biển báo giao
thông.

**Đầu ra:** - Ảnh kết quả có khung bao quanh vùng phát hiện. - Nhãn loại
biển báo và độ tin cậy dự đoán. - Thông tin tra cứu: mã, tên, nhóm, ý
nghĩa, mô tả hành vi cần tuân thủ. - Cảnh báo dạng văn bản dễ hiểu. -
Thông báo khi không phát hiện được biển hoặc độ tin cậy thấp.

Bài toán chính là object detection: xác định vị trí (bounding box) và
lớp (class) của biển báo. Nếu chỉ dùng ảnh đã cắt sẵn từng biển, bài
toán đó là image classification và không đủ đại diện cho kịch bản quét
ảnh đường phố.

## 1.4. Mục tiêu tổng quát

Thiết kế và triển khai một webapp có khả năng phát hiện, phân loại một
tập lớp biển báo giao thông Việt Nam trong ảnh, đồng thời trình bày
thông tin giải thích dựa trên cơ sở dữ liệu được biên soạn và kiểm
chứng.

## 1.5. Mục tiêu cụ thể

1.  Khảo sát bài toán và lựa chọn tập lớp phù hợp quy mô học kỳ.
2.  Chuẩn bị dữ liệu ảnh, nhãn bounding box và chia
    train/validation/test.
3.  Xây dựng pipeline tiền xử lý ảnh bằng OpenCV.
4.  Fine-tune mô hình object detection nhỏ.
5.  Đánh giá mô hình bằng Precision, Recall, F1 và mAP; ghi nhận tốc độ
    suy luận.
6.  Xây dựng API nhận ảnh, chạy suy luận và trả kết quả chuẩn hóa.
7.  Xây dựng webapp cho phép upload/chụp ảnh, xem kết quả và lịch sử.
8.  Đối chiếu nội dung giải thích biển báo với tài liệu pháp luật/nguồn
    chính thống.

## 1.6. Phạm vi phiên bản đồ án

### Bắt buộc (MVP)

-   Nhận ảnh JPG/JPEG/PNG.
-   Kiểm tra định dạng, dung lượng và kích thước ảnh.
-   Phát hiện và phân loại nhóm lớp biển báo đã chọn.
-   Vẽ bounding box, nhãn và confidence.
-   Hiển thị ý nghĩa và cảnh báo văn bản.
-   Có trạng thái không phát hiện/không chắc chắn.
-   Có trang mô tả dự án và nguồn dữ liệu.
-   Có báo cáo đánh giá mô hình.

### Nên có nếu còn thời gian

-   Chụp ảnh từ webcam/camera trình duyệt.
-   Lịch sử quét trong SQLite.
-   Xem chi tiết biển báo.
-   Bộ lọc lịch sử theo thời gian/lớp.
-   So sánh ảnh gốc và ảnh kết quả.

### Không đưa vào phạm vi cam kết

-   Nhận diện video thời gian thực liên tục.
-   Định vị GPS hoặc chỉ dẫn đường đi.
-   Cảnh báo âm thanh khi đang lái xe.
-   Nhận diện mọi biển báo Việt Nam.
-   Đưa ra kết luận pháp lý tự động cho mọi tình huống.
-   Nhận diện hành vi vi phạm của người điều khiển phương tiện.

## 1.7. Phạm vi lớp biển báo

Không nên chọn quá nhiều lớp ngay từ đầu. Đề xuất 10--20 lớp có dữ liệu
đủ tốt, ưu tiên các lớp trực quan và có ý nghĩa khác biệt rõ. Có thể tổ
chức theo nhóm: - Biển cấm. - Biển nguy hiểm/cảnh báo. - Biển hiệu
lệnh. - Biển chỉ dẫn.

Danh sách lớp cuối cùng phải phụ thuộc dữ liệu thực tế. Lập `class_id`,
`class_name`, `sign_code`, `group` thống nhất từ lúc gán nhãn đến lúc
hiển thị. Không tự suy đoán mã biển hoặc nội dung pháp lý.

## 1.8. Đối tượng sử dụng

-   Sinh viên và giảng viên dùng để minh họa nhận diện biển báo.
-   Người dùng phổ thông muốn tìm hiểu ý nghĩa biển báo qua ảnh.

## 1.9. Sản phẩm bàn giao

-   Mã nguồn frontend và backend.
-   Mô hình đã huấn luyện và cấu hình suy luận.
-   Tập dữ liệu hoặc hướng dẫn tải dữ liệu hợp pháp, kèm nguồn/giấy
    phép.
-   Cơ sở dữ liệu thông tin biển báo.
-   Tài liệu cài đặt và chạy.
-   Báo cáo đồ án, slide, kịch bản demo.
-   Bảng kết quả thực nghiệm và các giới hạn đã biết.

## 1.10. Câu hỏi nghiên cứu/thực nghiệm

-   Mô hình phát hiện được bao nhiêu lớp trong phạm vi dữ liệu?
-   Chất lượng thay đổi ra sao khi ảnh tối, mờ, nghiêng hoặc biển báo
    nhỏ?
-   Ngưỡng confidence ảnh hưởng thế nào đến Precision và Recall?
-   Tiền xử lý có cải thiện kết quả không? Chứng minh bằng thử nghiệm
    đối chứng thay vì khẳng định cảm tính.
-   Độ trễ xử lý một ảnh trên máy triển khai là bao nhiêu?

## 1.11. Giả thuyết và giới hạn

Giả thuyết: mô hình được fine-tune trên dữ liệu đại diện có thể nhận
diện các lớp đã chọn trong điều kiện gần với tập dữ liệu. Giới hạn: dữ
liệu ít, lệch lớp, khác biệt camera/thời tiết và vật cản có thể làm giảm
hiệu năng. Hệ thống chỉ hỗ trợ tham khảo.
