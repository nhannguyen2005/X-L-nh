# TrafficSign AI

## 1. Giới thiệu dự án

TrafficSign AI là hệ thống nhận diện và tra cứu biển báo giao thông Việt Nam dựa trên trí tuệ nhân tạo. Dự án được xây dựng nhằm hỗ trợ người dùng trong việc xác định loại biển báo từ hình ảnh đầu vào, đồng thời cung cấp thông tin mô tả, ý nghĩa và danh mục liên quan theo chuẩn giao thông Việt Nam.

Hệ thống bao gồm hai thành phần chính:
- Backend: xử lý API, nhận diện hình ảnh và truy xuất dữ liệu biển báo.
- Frontend: giao diện web để người dùng tải ảnh, xem kết quả và tra cứu thông tin.

## 2. Mục tiêu của dự án

- Tự động nhận diện biển báo giao thông từ ảnh đầu vào.
- Hỗ trợ tra cứu danh mục biển báo theo loại và ngữ cảnh.
- Cung cấp giao diện web thân thiện, dễ sử dụng.
- Tạo nền tảng cho các nghiên cứu, demo và mở rộng trong tương lai.

## 3. Công nghệ sử dụng

### Backend
- Python
- FastAPI
- Uvicorn
- OpenCV / xử lý hình ảnh (nếu được tích hợp trong mô hình)
- Tệp dữ liệu và trọng số mô hình AI

### Frontend
- React
- TypeScript
- Vite
- React Router

## 4. Cấu trúc thư mục

```bash
X-L-nh/
├── backend/
│   ├── app/
│   ├── data/
│   ├── static/
│   ├── tests/
│   ├── weights/
│   ├── .env
│   ├── .env.example
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── ...
├── artifacts/
├── TrafficSignAI_Documentation/
├── images/
├── run.sh
├── run.bat
├── run.ps1
├── stop.sh
├── stop.bat
├── README.md
├── he-thong-bien-bao.md
├── he-thong-bien-bao-01062020pdf_page-0001.pdf
└── ...
```

## 5. Yêu cầu môi trường

Trước khi chạy dự án, máy tính cần có:
- Python 3.10+
- Node.js 18+
- npm
- Git
- Trình duyệt web hiện đại

## 6. Hướng dẫn cài đặt

### 6.1 Clone dự án

```bash
git clone https://github.com/nhannguyen2005/X-L-nh.git
cd X-L-nh
```

### 6.2 Cài đặt backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Nếu dự án có file `.env`, hãy kiểm tra và chỉnh sửa cấu hình phù hợp trước khi chạy.

### 6.3 Cài đặt frontend

```bash
cd ../frontend
npm install
```

## 7. Hướng dẫn chạy dự án

### 7.1 Chạy nhanh bằng script

#### Windows
```bash
run.bat
```

#### PowerShell
```powershell
./run.ps1
```

#### Linux/macOS
```bash
chmod +x run.sh
./run.sh
```

Script trên sẽ tự động:
- kiểm tra môi trường Python
- cài đặt dependencies frontend nếu cần
- khởi động backend FastAPI trên cổng 8000
- khởi động frontend Vite trên cổng 5173
- mở trang web theo mặc định

### 7.2 Chạy thủ công

#### Terminal 1: Backend
```bash
cd backend
source .venv/bin/activate    # Windows: .venv\Scripts\activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Terminal 2: Frontend
```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

## 8. Cổng truy cập

Sau khi chạy thành công, hệ thống sẽ khả dụng tại:
- Giao diện web: http://127.0.0.1:5173
- Swagger/Docs API: http://127.0.0.1:8000/docs
- Tra cứu biển báo: http://127.0.0.1:5173/signs

## 9. Tắt ứng dụng

Bạn có thể dừng ứng dụng bằng cách:
- nhấn `Ctrl + C` trong các terminal đang chạy
- hoặc chạy file:
  - `stop.sh` cho Linux/macOS
  - `stop.bat` cho Windows

## 10. Tính năng chính

- Upload ảnh biển báo giao thông.
- Nhận dạng biển báo bằng mô hình AI.
- Hiển thị kết quả nhận diện lên giao diện web.
- Tra cứu danh mục biển báo theo tiêu chí phù hợp.
- Cung cấp tài liệu API để kiểm thử và tích hợp.

## 11. Lưu ý kỹ thuật

- Nếu gặp lỗi thiếu dependency, hãy chạy lại các lệnh cài đặt:
```bash
cd backend
pip install -r requirements.txt

cd ../frontend
npm install
```

- Nếu cần sửa cấu hình môi trường, hãy kiểm tra các file:
  - `backend/.env`
  - `backend/.env.example`

- Nếu hệ thống không khởi động, cần kiểm tra:
  - phiên bản Python và Node.js
  - cổng 8000 và 5173 chưa bị chiếm bởi tiến trình khác
  - thư mục `.venv` đã được tạo đúng cách

## 12. Ứng dụng trong báo cáo/đồ án

Dự án này phù hợp để trình bày trong các báo cáo học thuật hoặc đồ án công nghệ vì có các yếu tố sau:
- xác định rõ mục tiêu giải quyết bài toán
- ứng dụng AI vào bài toán thực tế
- có frontend và backend tách riêng
- có khả năng mở rộng cho các tính năng nâng cao
- có giao diện trực quan và dễ kiểm thử

## 13. Kết luận

TrafficSign AI là một dự án ứng dụng trí tuệ nhân tạo trong lĩnh vực giao thông, hướng tới việc hỗ trợ nhận diện và tra cứu biển báo giao thông Việt Nam. Dự án không chỉ thể hiện tính ứng dụng thực tế mà còn có tiềm năng phát triển mạnh trong bối cảnh công nghệ nhận diện hình ảnh và hệ thống thông minh ngày càng phổ biến.

## 14. Tham khảo

- Tài liệu về FastAPI: https://fastapi.tiangolo.com/
- Tài liệu về React: https://react.dev/
- Tài liệu về Vite: https://vitejs.dev/
- Quy chuẩn biển báo giao thông Việt Nam: `he-thong-bien-bao.md`
