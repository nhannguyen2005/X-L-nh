# 2. Đặc tả yêu cầu

## 2.1. Vai trò

-   **Khách truy cập/người dùng:** gửi ảnh, xem kết quả, xem thông tin
    biển báo, xem lịch sử nếu tính năng được bật.
-   **Quản trị nội dung (tùy chọn):** cập nhật nội dung mô tả biển báo
    và nguồn tham khảo.
-   **Nhóm phát triển:** quản lý dữ liệu, mô hình, cấu hình và log.

Không cần xây hệ thống tài khoản/phân quyền phức tạp cho MVP nếu giảng
viên không yêu cầu.

## 2.2. Yêu cầu chức năng

  -----------------------------------------------------------------------
  ID                Yêu cầu           Mức độ            Tiêu chí nghiệm
                                                        thu
  ----------------- ----------------- ----------------- -----------------
  FR-01             Tải ảnh lên       Must              Chấp nhận JPG/PNG
                                                        hợp lệ

  FR-02             Kiểm tra ảnh      Must              Từ chối file sai
                                                        định dạng/quá
                                                        dung lượng/không
                                                        giải mã được

  FR-03             Tiền xử lý        Must              Ảnh được chuẩn
                                                        hóa theo pipeline
                                                        đã mô tả

  FR-04             Phát hiện biển    Must              Trả bounding box
                    báo                                 cho mỗi detection
                                                        hợp lệ

  FR-05             Phân loại         Must              Trả class ID, tên
                                                        lớp, confidence

  FR-06             Tra cứu thông tin Must              Nhãn hợp lệ liên
                                                        kết đúng bản ghi

  FR-07             Hiển thị cảnh báo Must              Hiển thị mô tả,
                                                        khuyến nghị và
                                                        mức cảnh báo đã
                                                        biên soạn

  FR-08             Trường hợp không  Must              Thông báo rõ,
                    phát hiện                           không hiển thị
                                                        kết quả giả

  FR-09             Confidence thấp   Must              Gắn trạng thái
                                                        cần xác minh,
                                                        không khẳng định
                                                        chắc chắn

  FR-10             Lịch sử quét      Should            Lưu thời gian,
                                                        tên file, số
                                                        detection, trạng
                                                        thái

  FR-11             Camera trình      Could             Chụp ảnh khi
                    duyệt                               người dùng cấp
                                                        quyền

  FR-12             Trang giới        Should            Nêu phạm vi, giới
                    thiệu/nguồn                         hạn, nguồn dữ
                                                        liệu/pháp lý
  -----------------------------------------------------------------------

## 2.3. Yêu cầu phi chức năng

-   **Hiệu năng:** ghi nhận thời gian xử lý; không đặt mục tiêu tùy tiện
    trước khi đo trên máy thực tế.
-   **Độ tin cậy:** API trả lỗi có cấu trúc; không làm sập server khi
    ảnh lỗi.
-   **Bảo mật:** giới hạn dung lượng, kiểm tra MIME và nội dung thực,
    tên file do server sinh, không thực thi file upload.
-   **Quyền riêng tư:** mặc định không lưu ảnh gốc lâu dài; thông báo
    nếu có lưu.
-   **Khả dụng:** giao diện có trạng thái đang xử lý, thành công, lỗi,
    không phát hiện.
-   **Bảo trì:** tách model inference, xử lý ảnh, dữ liệu biển báo và
    API.
-   **Khả năng tái lập:** lưu phiên bản dataset, cấu hình, seed và
    checkpoint.
-   **Tương thích:** kiểm thử trên trình duyệt desktop hiện đại; camera
    chỉ chạy trên HTTPS hoặc localhost.

## 2.4. Quy tắc nghiệp vụ

1.  Chỉ hiển thị thông tin pháp lý khi class ID ánh xạ tới bản ghi đã
    kiểm chứng.
2.  Nếu confidence thấp hơn ngưỡng cấu hình, hiển thị "Kết quả chưa chắc
    chắn".
3.  Không phát hiện biển báo không đồng nghĩa ảnh không có biển báo.
4.  Nếu mô hình trả nhiều box trùng, áp dụng NMS theo cấu hình mô hình.
5.  Một ảnh có thể chứa nhiều biển báo; không giả định chỉ có một
    detection.
6.  Không suy ra hành vi vi phạm chỉ từ một biển báo; ngữ cảnh đường và
    biển phụ có thể quan trọng.
7.  Nội dung cảnh báo phải mô tả đúng ý nghĩa, tránh diễn đạt như tư vấn
    pháp lý cá nhân.

## 2.5. Tiêu chí nghiệm thu tổng thể

-   Chạy được theo tài liệu cài đặt trên máy khác.
-   Upload ảnh hợp lệ và nhận JSON kết quả.
-   Ảnh kết quả có bounding box đúng tọa độ.
-   Tra cứu đúng thông tin cho tất cả lớp đã công bố.
-   Có thông báo rõ cho ảnh lỗi, ảnh không có biển, confidence thấp.
-   Có tập test độc lập và bảng chỉ số.
-   Báo cáo nêu giới hạn, không che giấu lỗi.
-   Demo được tối thiểu 5 tình huống đã chuẩn bị.
