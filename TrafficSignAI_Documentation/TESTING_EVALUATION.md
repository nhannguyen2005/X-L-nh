# 9. Kiểm thử và đánh giá

## 9.1. Hai nhóm đánh giá

1.  **Đánh giá mô hình:** đo chất lượng phát hiện/phân loại trên tập
    test độc lập.
2.  **Kiểm thử phần mềm:** xác nhận API, frontend, database và xử lý lỗi
    hoạt động đúng.

Không dùng accuracy phân loại đơn lẻ để đánh giá detector nếu bài toán
có bounding box.

## 9.2. Chỉ số mô hình

-   Precision = TP / (TP + FP).
-   Recall = TP / (TP + FN).
-   F1 = 2 × Precision × Recall / (Precision + Recall).
-   IoU = diện tích giao / diện tích hợp giữa box dự đoán và ground
    truth.
-   mAP@0.5: mean Average Precision tại IoU 0.5.
-   mAP@0.5:0.95: trung bình AP qua nhiều ngưỡng IoU.

Báo cáo cả chỉ số tổng và theo từng lớp nếu công cụ hỗ trợ. Ghi rõ cách
tính, ngưỡng và phiên bản evaluator.

## 9.3. Ma trận kiểm thử chức năng

  -----------------------------------------------------------------------
  ID                      Đầu vào                 Kết quả mong đợi
  ----------------------- ----------------------- -----------------------
  TC-01                   JPG hợp lệ có một biển  Phát hiện, box và thông
                          rõ                      tin đúng

  TC-02                   PNG hợp lệ có nhiều     Trả nhiều detection
                          biển                    

  TC-03                   Ảnh không có biển       detection_count = 0,
                                                  thông báo phù hợp

  TC-04                   File văn bản đổi đuôi   Bị từ chối
                          .jpg                    

  TC-05                   Ảnh vượt giới hạn       HTTP 413

  TC-06                   Ảnh bị hỏng             INVALID_IMAGE

  TC-07                   Biển nhỏ/xa             Ghi nhận đúng kết quả,
                                                  không ép phải phát hiện

  TC-08                   Ảnh tối/mờ              Hiển thị kết quả hoặc
                                                  trạng thái không chắc
                                                  chắn

  TC-09                   Confidence dưới         Không hiển thị như kết
                          threshold               quả chắc chắn

  TC-10                   Model không có weights  Health báo chưa sẵn
                                                  sàng, API trả lỗi rõ

  TC-11                   Catalog thiếu class     Hiển thị nhãn chưa có
                                                  thông tin, không crash

  TC-12                   Gọi API liên tiếp       Không load model lại
                                                  mỗi request
  -----------------------------------------------------------------------

## 9.4. Phân tích lỗi định tính

Tạo bộ ảnh gồm: - Biển rõ, chính diện. - Biển nghiêng. - Biển nhỏ/xa. -
Thiếu sáng/ngược sáng. - Bị che khuất. - Nền phức tạp hoặc có biển quảng
cáo giống biển báo. - Ảnh không chứa biển.

Với mỗi lỗi, ghi: ảnh, nhãn thật, dự đoán, confidence, nguyên nhân khả
dĩ, hướng cải thiện. Không chỉ chọn các ảnh mô hình nhận diện tốt để đưa
vào báo cáo.

## 9.5. Đo tốc độ

Đo riêng: - Decode/validation. - Preprocessing. - Inference. -
Postprocessing/render. - Tổng thời gian server.

Chạy warm-up trước khi đo, đo nhiều lần và báo cáo trung vị hoặc trung
bình kèm số lần thử. Ghi CPU/GPU, kích thước ảnh, model input size và
cấu hình máy.

## 9.6. Ablation study

Nếu thời gian cho phép, so sánh: - Baseline không CLAHE. - Baseline +
CLAHE. - Baseline + augmentation đã chọn. - Các ngưỡng confidence khác
nhau.

Giữ cùng tập test và điều kiện đo. Chỉ kết luận kỹ thuật có ích khi số
liệu hỗ trợ.

## 9.7. Unit/integration tests

-   Test kiểm tra ảnh và giới hạn file.
-   Test quy đổi tọa độ letterbox.
-   Test mapping class ID → catalog.
-   Test schema response.
-   Test endpoint bằng ảnh fixture.
-   Test trường hợp model chưa load.
-   Test dữ liệu history và phân trang.

## 9.8. Bảng kết quả cần điền

  Thử nghiệm       Precision   Recall    F1   mAP50   mAP50-95   Latency
  -------------- ----------- -------- ----- ------- ---------- ---------
  Baseline               TBD      TBD   TBD     TBD        TBD       TBD
  Thử nghiệm 2           TBD      TBD   TBD     TBD        TBD       TBD

Không để TBD trong bản báo cáo nộp cuối. Nếu một chỉ số không tính được,
giải thích lý do.
