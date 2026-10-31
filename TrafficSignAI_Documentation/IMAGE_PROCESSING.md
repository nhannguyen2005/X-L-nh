# 4. Quy trình xử lý ảnh

## 4.1. Mục tiêu

Chuẩn hóa ảnh đầu vào, hỗ trợ mô hình phát hiện biển báo và tạo ảnh kết
quả dễ quan sát. Phải phân biệt bước tiền xử lý bắt buộc với bước thử
nghiệm; không áp dụng mọi bộ lọc một cách máy móc vì xử lý quá mức có
thể làm mất đặc trưng.

## 4.2. Pipeline đề xuất

``` text
Ảnh đầu vào
  -> kiểm tra/giải mã
  -> chuẩn hóa kênh màu
  -> resize/letterbox theo yêu cầu model
  -> inference
  -> quy đổi tọa độ về ảnh gốc
  -> lọc confidence + NMS (theo model)
  -> vẽ bounding box/nhãn
  -> trả kết quả
```

## 4.3. Các kỹ thuật cần trình bày trong báo cáo

### Đọc và biểu diễn ảnh

Ảnh màu thường được biểu diễn bằng ma trận pixel với ba kênh. OpenCV mặc
định đọc ảnh màu theo thứ tự BGR, trong khi nhiều thư viện hiển thị dùng
RGB. Cần chuyển đổi đúng trước khi truyền dữ liệu giữa các thư viện.

### Resize và letterbox

Model thường yêu cầu kích thước đầu vào cố định hoặc giới hạn. Resize
trực tiếp có thể làm méo hình; letterbox giữ tỷ lệ khung hình bằng cách
co ảnh và thêm padding. Khi model trả bounding box trên ảnh letterbox,
phải loại padding và quy đổi tọa độ về ảnh gốc.

### Chuẩn hóa

Chuẩn hóa pixel theo cách model yêu cầu (ví dụ scale về \[0,1\]). Không
tự ý chuẩn hóa hai lần nếu framework đã thực hiện nội bộ.

### Tăng cường dữ liệu (augmentation)

Có thể thử thay đổi độ sáng/độ tương phản, blur nhẹ, xoay nhỏ, scale,
crop và biến đổi phối cảnh. Augmentation phải hợp lý với biển báo; không
dùng biến đổi làm thay đổi ý nghĩa lớp. Ví dụ lật ngang có thể không hợp
lệ với biển có ký hiệu định hướng hoặc chữ/số.

### Chuyển đổi không gian màu

HSV tách Hue/Saturation/Value, hữu ích để khảo sát màu sắc; grayscale hỗ
trợ một số phép phân tích biên. Đây là bước nghiên cứu/đối chứng, không
mặc định thay thế ảnh màu đầu vào của detector.

### Làm mờ và khử nhiễu

Gaussian blur giảm nhiễu tần số cao nhưng cũng làm mờ biên và ký hiệu.
Chỉ áp dụng nếu thực nghiệm chứng minh có lợi. Có thể so sánh ảnh gốc và
ảnh xử lý trong phần đánh giá.

### Cân bằng sáng

CLAHE có thể cải thiện tương phản cục bộ trong ảnh thiếu sáng, nhưng có
thể khuếch đại nhiễu. Đưa vào thử nghiệm ablation, không bật mặc định
nếu chưa đo.

## 4.4. Phát hiện đối tượng và hậu xử lý

Mô hình detector dự đoán bounding box, class và confidence. Non-Maximum
Suppression (NMS) loại các box chồng lấn cao cho cùng đối tượng. IoU
giữa hai box: `IoU = diện tích giao / diện tích hợp`.

Ngưỡng confidence điều khiển mức chắc chắn tối thiểu để giữ detection.
Ngưỡng IoU ảnh hưởng loại box trùng. Hai ngưỡng này phải được lựa chọn
trên validation, sau đó cố định khi đánh giá test.

## 4.5. Thông số cần lưu

-   Kích thước ảnh gốc và kích thước model input.
-   Phương pháp resize/letterbox.
-   Ngưỡng confidence và IoU.
-   Phiên bản thư viện OpenCV/framework.
-   Thời gian tiền xử lý, inference, hậu xử lý riêng biệt.
-   Thiết bị CPU/GPU và cấu hình máy.

## 4.6. Thí nghiệm đối chứng

Thực hiện ít nhất: - A: pipeline cơ sở, không thêm tăng cường lúc
inference. - B: thử CLAHE hoặc cân bằng sáng trên ảnh khó. - C: thử một
phương pháp khử nhiễu phù hợp.

So sánh mAP/Recall và thời gian. Nếu không cải thiện, giữ pipeline đơn
giản và ghi nhận kết quả đó. Augmentation trong huấn luyện phải tách
biệt với preprocessing khi inference.
