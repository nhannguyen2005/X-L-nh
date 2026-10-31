# 11. Hướng dẫn viết báo cáo đồ án

## Bố cục đề xuất

### Trang bìa, lời cảm ơn, nhận xét

Theo mẫu của khoa/trường. Kiểm tra quy định định dạng, số trang, trích
dẫn.

### Chương 1 --- Giới thiệu đề tài

-   Bối cảnh và lý do chọn đề tài.
-   Mục tiêu tổng quát/cụ thể.
-   Đối tượng, phạm vi và giới hạn.
-   Phương pháp thực hiện.
-   Bố cục báo cáo.

### Chương 2 --- Cơ sở lý thuyết

-   Biểu diễn ảnh số, pixel, RGB/BGR.
-   Resize, chuẩn hóa, letterbox.
-   Augmentation và các kỹ thuật xử lý ảnh đã thực sự sử dụng.
-   Bài toán object detection.
-   Bounding box, IoU, confidence, NMS.
-   Kiến trúc mô hình được chọn ở mức cần thiết.
-   Precision, Recall, F1, mAP.

Không chép lý thuyết dài không liên quan. Mỗi kỹ thuật cần nối với cách
áp dụng trong hệ thống.

### Chương 3 --- Phân tích và thiết kế

-   Yêu cầu chức năng/phi chức năng.
-   Use case và luồng xử lý.
-   Kiến trúc frontend/backend/model/database.
-   Thiết kế API.
-   Thiết kế cơ sở dữ liệu.
-   Quy trình xử lý ảnh.

### Chương 4 --- Dữ liệu và huấn luyện

-   Nguồn và giấy phép dataset.
-   Danh sách lớp.
-   Quy trình gán nhãn, chia tập.
-   Thống kê dữ liệu bằng biểu đồ.
-   Cấu hình huấn luyện và môi trường.
-   Các thí nghiệm và lựa chọn checkpoint.

### Chương 5 --- Cài đặt và kết quả

-   Công nghệ và cấu trúc chương trình.
-   Các màn hình/chức năng thực tế.
-   Ví dụ detection thành công và thất bại.
-   Bảng metrics tổng và theo lớp.
-   Đo thời gian xử lý.
-   Kiểm thử API/chức năng.
-   Phân tích lỗi và giới hạn.

### Chương 6 --- Kết luận và hướng phát triển

-   Mức độ hoàn thành mục tiêu.
-   Kết quả định lượng thực tế.
-   Hạn chế.
-   Hướng phát triển khả thi: thêm lớp, dữ liệu đa điều kiện, video, tối
    ưu model.

### Tài liệu tham khảo và phụ lục

-   Tài liệu framework, paper, dataset, văn bản pháp luật.
-   Hướng dẫn chạy.
-   API sample.
-   Bảng phân công (nếu làm nhóm).
-   Ảnh kết quả và log thực nghiệm.

## Hình/bảng nên có

1.  Sơ đồ pipeline xử lý ảnh.
2.  Sơ đồ kiến trúc hệ thống.
3.  Thống kê số ảnh/instance theo lớp.
4.  Ví dụ ảnh gán nhãn.
5.  Biểu đồ loss và mAP theo epoch.
6.  Confusion matrix hoặc PR curve.
7.  Bảng Precision/Recall/F1/mAP.
8.  Bảng latency.
9.  Ảnh demo kết quả tốt và lỗi.

## Nguyên tắc trình bày kết quả

-   Nêu rõ tập dữ liệu, số ảnh, số instance và phiên bản model.
-   Nêu rõ test độc lập.
-   Không làm tròn quá mức để tạo cảm giác chính xác.
-   Phân biệt kết quả model với chất lượng nội dung catalog.
-   Nếu dùng model pretrained, ghi rõ nguồn và quá trình fine-tune.
-   Trích dẫn nguồn dataset, framework, hình ảnh và văn bản pháp lý.

## Câu hỏi giảng viên có thể hỏi

-   Vì sao chọn object detection thay vì classification?
-   Vì sao chọn YOLO bản nhỏ?
-   Dữ liệu lấy ở đâu, có bao nhiêu lớp?
-   Gán nhãn bounding box như thế nào?
-   Vì sao cần train/validation/test?
-   IoU, NMS, confidence và mAP là gì?
-   Nếu ảnh không có biển hoặc có nhiều biển thì sao?
-   Làm sao tránh model nhận diện nhầm quảng cáo thành biển?
-   Vì sao cần tiền xử lý? Có chứng minh cải thiện không?
-   Model chạy trên CPU/GPU nào, latency bao nhiêu?
-   Hệ thống xử lý ra sao khi confidence thấp?
-   Nội dung pháp lý lấy từ đâu và kiểm chứng thế nào?
