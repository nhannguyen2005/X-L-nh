# TrafficSign AI

Dự án nhận diện và tra cứu biển báo giao thông Việt Nam bằng AI.

## Yêu cầu môi trường

- Python 3.10+
- Node.js 18+
- npm
- Git

## Cài đặt nhanh

### 1. Clone dự án

```bash
git clone https://github.com/nhannguyen2005/X-L-nh.git
cd X-L-nh
```

### 2. Thiết lập Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Thiết lập Frontend

```bash
cd ../frontend
npm install
```

## Chạy dự án

### Cách nhanh nhất

- Windows: chạy file `run.bat`
- Linux/macOS: chạy file `run.sh`

Ví dụ:

```bash
chmod +x run.sh
./run.sh
```

### Chạy thủ công

Mở 2 terminal riêng:

#### Terminal 1 - Backend

```bash
cd backend
source .venv/bin/activate   # hoặc .venv\Scripts\activate trên Windows
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Terminal 2 - Frontend

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

## Truy cập ứng dụng

- Web: http://127.0.0.1:5173
- API docs: http://127.0.0.1:8000/docs
- Tra cứu biển báo: http://127.0.0.1:5173/signs

## Dừng dự án

- Nhấn `Ctrl + C` ở từng terminal đang chạy
- Hoặc chạy file:
  - `stop.sh` (Linux/macOS)
  - `stop.bat` (Windows)

## Lưu ý

- Backend có file `.env` để cấu hình môi trường nếu cần.
- Nếu gặp lỗi thiếu package, hãy chạy lại `pip install -r requirements.txt` hoặc `npm install`.
- Nếu cần chạy trên Windows PowerShell, có thể dùng `run.ps1`.

## Tóm tắt

- Backend: FastAPI
- Frontend: React + Vite
- Port mặc định: 8000 (API), 5173 (web)
