# TrafficSign AI - Giao Diện Người Dùng (Frontend)

Ứng dụng web nhận diện biển báo giao thông Việt Nam theo chuẩn **QCVN 41:2019/BGTVT**, được xây dựng với **React 19**, **TypeScript**, **Vite** và **Vanilla CSS Tokens** (tuân thủ nghiêm ngặt theo tài liệu `UI_UX.md`).

---

## 🎨 Điểm Nổi Bật Thiết Kế & Trải Nghiệm (UI/UX)

- **Bộ màu chuẩn hóa**:
  - Tông chủ đạo: Teal `#0F766E` (gợi mở công nghệ giao thông thông minh, chuyên nghiệp).
  - Màu nhóm biển chuẩn: Biển cấm `#C8102E`, Nguy hiểm/Cảnh báo `#F2B705`, Hiệu lệnh `#0B5CAD`, Chỉ dẫn `#1E3A8A`.
- **Typography self-hosted**:
  - `Be Vietnam Pro` cho tiêu đề và nội dung chữ.
  - `JetBrains Mono` cho mã hiệu biển (P.102, W.201a), tọa độ bbox, confidence score, và latency.
- **Biểu tượng hình học trừu tượng (Geometric SignGlyphs)**: Biểu diễn hình học tối giản, chính xác về hình dáng (tròn viền đỏ, tam giác viền đỏ, tròn xanh, chữ nhật xanh) thay vì emoji.
- **Tương tác 2 chiều trên Canvas**: Bbox SVG vector tương tác đồng bộ với danh sách thẻ kết quả bên cạnh (hover/click highlight).
- **Tuân thủ đạo đức học thuật**: Không tạo số liệu giả, cảnh báo rõ ràng khi model weights chưa sẵn sàng, hiển thị thông điệp học thuật và căn cứ pháp lý quy chuẩn rõ ràng.

---

## 🚀 Cài Đặt và Khởi Chạy

### 1. Cài đặt dependencies
```bash
npm install
```

### 2. Chạy môi trường Development
```bash
npm run dev
```
Ứng dụng sẽ chạy tại: [http://127.0.0.1:5173](http://127.0.0.1:5173).  
Vite dev server đã được cấu hình proxy tự động chuyển tiếp các request `/api` đến backend tại `http://127.0.0.1:8000`.

### 3. Build kiểm tra và đóng gói Production
```bash
npm run build
```
Kết quả đóng gói nằm tại thư mục `dist/`.

---

## 🧭 Cấu Trúc Các Màn Hình

1. **Quét ảnh (`/`)**:
   - Hero ngắn gọn, hỗ trợ Kéo/Thả ảnh (Dropzone) hoặc Chụp trực tiếp từ Webcam.
   - Thanh trượt điều chỉnh ngưỡng tin cậy (Confidence threshold: 0.1 - 0.9).
   - Tùy chọn lưu lịch sử quét vào SQLite (mặc định tắt theo quyền riêng tư).
   - Hiển thị kết quả tương tác 2 chiều: Canvas ảnh SVG + Thẻ phân tích hành vi & quy chuẩn.
2. **Tra cứu biển báo (`/signs`)**:
   - Tìm kiếm theo mã (`P.102`, `W.201a`...) hoặc tên biển.
   - Lọc theo nhóm danh mục biển (Biển cấm, Biển nguy hiểm, Biển hiệu lệnh, Biển chỉ dẫn) kèm số lượng.
   - Phân trang mượt mà.
3. **Chi tiết biển báo (`/signs/:id`)**:
   - Breadcrumb điều hướng.
   - Ý nghĩa quy chuẩn chi tiết theo QCVN 41:2019/BGTVT.
   - Hành vi tuân thủ & khuyến nghị an toàn cho người điều khiển phương tiện kèm mức cảnh báo (Low/Medium/High).
   - Nguồn văn bản pháp lý và ngày kiểm chứng dữ liệu.
4. **Lịch sử quét (`/history`)**:
   - Tìm kiếm lịch sử, phân trang.
   - Xem lại chi tiết từng lượt nhận diện, xóa bản ghi hoặc xóa toàn bộ lịch sử.
5. **Hiệu năng mô hình (`/metrics`)**:
   - Báo cáo định lượng thực nghiệm (Precision, Recall, mAP50, mAP50-95, Latency).
   - Bento grid và bảng per-class metrics từ dữ liệu đo đạc thực tế (`evaluation.json`).
6. **Giới thiệu & Căn cứ quy chuẩn (`/about`)**:
   - Giới hạn hệ thống (mục đích học thuật, thời tiết, góc chụp).
   - Danh sách 23 lớp biển báo trong phạm vi nghiên cứu.
   - Căn cứ pháp lý QCVN 41:2019/BGTVT.
   - Tech stack chi tiết.
