# 12. Kịch bản demo và bảo vệ

## 12.1. Chuẩn bị trước buổi demo

-   [ ] Cài dependencies và chạy thử trên đúng máy trình bày.
-   [ ] Kiểm tra file weights và catalog.
-   [ ] Kiểm tra backend health.
-   [ ] Kiểm tra frontend kết nối đúng API.
-   [ ] Chuẩn bị 5--8 ảnh demo có nguồn hợp pháp.
-   [ ] Có ảnh một biển rõ, nhiều biển, ảnh không có biển, ảnh tối/mờ và
    ảnh lỗi.
-   [ ] Chuẩn bị kết quả dự phòng dạng ảnh/video nếu mạng hoặc camera
    gặp sự cố.
-   [ ] Tắt thông báo không liên quan.
-   [ ] Không phụ thuộc Internet nếu mô hình chạy local.

## 12.2. Kịch bản trình diễn 5--7 phút

1.  Giới thiệu bài toán và phạm vi lớp.
2.  Mở trang web, giải thích quy trình.
3.  Upload ảnh có một biển rõ; chỉ vị trí box và confidence.
4.  Giải thích thông tin biển báo và khuyến nghị.
5.  Upload ảnh có nhiều biển.
6.  Upload ảnh không có biển hoặc ảnh khó; trình bày giới hạn và trạng
    thái confidence.
7.  Mở phần kết quả đánh giá mô hình; nêu dataset, test set, mAP và
    latency.
8.  Kết luận: chức năng hoàn thành và hướng phát triển.

## 12.3. Nguyên tắc demo

-   Không chỉ demo ảnh mà mô hình đã nhìn thấy trong train.
-   Không che giấu trường hợp nhận diện sai.
-   Không nói "chính xác tuyệt đối".
-   Nói rõ đây là prototype hỗ trợ học tập.
-   Khi kết quả sai, giải thích khả năng nguyên nhân: dữ liệu, kích
    thước vật thể, góc chụp, ánh sáng, che khuất hoặc lớp gần giống.

## 12.4. Phương án dự phòng

-   Lưu sẵn một vài response JSON để minh họa API nếu model khởi động
    chậm.
-   Lưu ảnh kết quả đã tạo từ lần chạy thật.
-   Có bản ghi video demo ngắn.
-   Tuy nhiên, phải nói rõ khi dùng dữ liệu ghi sẵn; không giả làm xử lý
    trực tiếp.
