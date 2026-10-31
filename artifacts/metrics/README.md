# TrafficSign AI - Evaluation Artifacts & Metrics

Thư mục chứa kết quả đo lường, đánh giá mô hình trên tập test độc lập theo quy định tại `TESTING_EVALUATION.md` và `UI_UX.md §14.7.4`.

## Các tệp được backend phục vụ tự động:
1. `evaluation.json`: Số liệu kiểm thử định lượng:
   - `experiment`: dataset name, dataset version, test images, test instances, model name, conf_threshold, iou_threshold, device
   - `metrics`: precision, recall, f1, map50, map50_95
   - `latency`: preprocess_ms, inference_ms, postprocess_ms, total_ms, runs_count
   - `classes`: danh sách metrics theo từng lớp biển báo
2. `results.csv`: Log chi tiết theo epoch
3. `confusion_matrix.png`: Biểu đồ ma trận nhầm lẫn
4. `PR_curve.png`: Đường cong Precision-Recall
5. `F1_curve.png`: Đường cong F1 theo ngưỡng confidence
