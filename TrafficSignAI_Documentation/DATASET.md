# 5. Dữ liệu và gán nhãn

## 5.1. Nguyên tắc lựa chọn

Chất lượng và tính phù hợp của dataset quan trọng hơn số lượng ảnh lớn
nhưng nhãn sai. Chọn dữ liệu có giấy phép rõ, nguồn truy xuất được, ảnh
đại diện bối cảnh thực tế và đủ ví dụ cho từng lớp.

Có thể khảo sát: - Dataset biển báo Việt Nam do nhóm/đơn vị nghiên cứu
công bố. - Dataset công khai trên Roboflow Universe hoặc Kaggle: phải
kiểm tra license, nguồn gốc và điều kiện sử dụng từng bộ. - Ảnh tự chụp:
chỉ sử dụng ảnh do nhóm có quyền sử dụng; tránh chụp gây mất an toàn
giao thông. - Dataset quốc tế như GTSRB/GTSDB chỉ dùng tham khảo kỹ
thuật; không mặc định thay thế biển báo Việt Nam.

Không tải hoặc phân phối lại dataset nếu giấy phép không cho phép. Ghi
URL nguồn, ngày truy cập, tác giả, license và điều kiện sử dụng.

## 5.2. Phạm vi lớp

Bắt đầu với khoảng 10--20 lớp có đủ ảnh. Tạo `classes.csv` với các cột:
`class_id,class_name,sign_code,sign_group,description,source`.

Quy tắc: - ID liên tục từ 0. - Tên lớp duy nhất, không nhập nhằng. -
Không đổi thứ tự ID sau khi huấn luyện. - Lưu mapping cùng checkpoint. -
Nếu hai loại biển quá giống nhau hoặc dữ liệu thiếu, cân nhắc gộp ở cấp
nhóm hoặc loại khỏi MVP.

## 5.3. Gán nhãn object detection

Mỗi biển báo nhìn thấy được gán một bounding box sát đối tượng. Với YOLO
format, mỗi dòng: `class_id x_center y_center width height` Trong đó tọa
độ được chuẩn hóa về \[0,1\] theo chiều rộng/cao ảnh.

Kiểm tra: - Box không có chiều rộng/cao bằng 0. - Tọa độ nằm trong biên
ảnh. - Class ID nằm trong danh sách lớp. - Box không bao gồm quá nhiều
nền. - Quy tắc nhất quán cho biển bị che khuất/cắt khỏi ảnh. - Ảnh không
có biển có file label rỗng nếu pipeline yêu cầu.

## 5.4. Chia train/validation/test

Tách dữ liệu theo ảnh hoặc theo nguồn/cảnh quay để tránh leakage. Nếu
nhiều frame liên tiếp từ cùng video, không chia ngẫu nhiên các frame gần
nhau sang cả train và test.

Tỷ lệ tham khảo: 70% train, 15% validation, 15% test. Có thể thay đổi
theo quy mô dataset, nhưng phải nêu lý do. Test chỉ dùng đánh giá cuối
cùng; không dùng để chọn hyperparameter.

## 5.5. Kiểm tra mất cân bằng

Thống kê: - Số ảnh theo lớp. - Số instance theo lớp. - Số ảnh không có
đối tượng. - Phân bố kích thước box. - Điều kiện ánh sáng/thời tiết/góc
chụp nếu có metadata.

Không chỉ nhìn số ảnh; một ảnh có thể chứa nhiều instance. Bổ sung dữ
liệu cho lớp hiếm hoặc điều chỉnh sampling có kiểm soát.

## 5.6. Cấu trúc dataset

``` text
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
├── data.yaml
├── classes.csv
└── DATASET_CARD.md
```

Ví dụ `data.yaml` (thay tên lớp theo bộ dữ liệu thực):

``` yaml
path: ../dataset
train: images/train
val: images/val
test: images/test
names:
  0: cam_di_nguoc_chieu
  1: cam_re_trai
  2: nguy_hiem_giao_nhau
```

## 5.7. Dataset card phải có

-   Tên dataset và phiên bản.
-   Nguồn tải, ngày truy cập, license.
-   Tổng ảnh và tổng instance.
-   Danh sách lớp.
-   Quy trình gán nhãn.
-   Cách chia tập.
-   Các hạn chế/thiên lệch.
-   Những bước tiền xử lý đã thực hiện.

## 5.8. Kiểm tra chất lượng

Trước huấn luyện, chạy script kiểm tra file ảnh đọc được, file label tồn
tại, class ID hợp lệ, box trong biên, ảnh trùng lặp và phân bố lớp. Lưu
báo cáo kiểm tra để đưa vào phụ lục.
