@echo off
chcp 65001 >nul
title Khởi động TrafficSign AI
color 0B

echo.
echo ====================================================================
echo               TRAFFICSIGN AI - HE THONG KHOI DONG DANG
echo       He thong Nhan dien ^& Tra cuu Bien bao Giao thong Viet Nam
echo ====================================================================
echo.

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

:: 1. Kiem tra Python va moi truong ao Backend
set "PYTHON_EXE=%ROOT_DIR%backend\.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
    echo [CANH BAO] Khong tim thay moi truong ao tai backend\.venv.
    echo Dang thu su dung Python toan cuc...
    set "PYTHON_EXE=python"
)

:: 2. Kiem tra thu muc node_modules cua Frontend
if not exist "%ROOT_DIR%frontend\node_modules" (
    echo [THONG BAO] Dang cai dat thu vien Frontend (npm install)...
    cd /d "%ROOT_DIR%frontend"
    call npm install
    cd /d "%ROOT_DIR%"
)

:: 3. Khoi dong Backend FastAPI tai cong 8000
echo [1/3] Dang khoi dong Backend FastAPI (http://127.0.0.1:8000)...
start "TrafficSign AI - Backend [Port 8000]" /D "%ROOT_DIR%backend" cmd /k ""%PYTHON_EXE%" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

:: 4. Khoi dong Frontend Vite tai cong 5173
echo [2/3] Dang khoi dong Frontend Vite (http://127.0.0.1:5173)...
start "TrafficSign AI - Frontend [Port 5173]" /D "%ROOT_DIR%frontend" cmd /k "npm run dev -- --host 127.0.0.1 --port 5173"

:: 5. Cho server khoi dong va tu dong mo trinh duyet
echo [3/3] Cho he thong san sang trong 4 giay...
timeout /t 4 /nobreak >nul

echo Dang mo giao dien tren trinh duyet...
start http://127.0.0.1:5173

echo.
echo ====================================================================
echo                  HE THONG DA KHOI DONG THANH CONG!
echo.
echo  * Giao dien Web nguoi dung : http://127.0.0.1:5173
echo  * Tai lieu Backend Swagger : http://127.0.0.1:8000/docs
echo  * Tra cuu danh muc 65 bien : http://127.0.0.1:5173/signs
echo.
echo  * Luu y: De tat he thong, dong 2 cua so Backend va Frontend
echo          hoac nhap dup chuot vao file stop.bat
echo ====================================================================
echo.
pause
