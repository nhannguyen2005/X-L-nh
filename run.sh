#!/usr/bin/env bash

# ====================================================================
#               TRAFFICSIGN AI - SCRIPT KHOI DONG BASH
#       He thong Nhan dien & Tra cuu Bien bao Giao thong Viet Nam
# ====================================================================

set -e

# Mau sac terminal
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "===================================================================="
echo "           TRAFFICSIGN AI - KHOI DONG TOAN BO DU AN"
echo "   Backend: FastAPI (Port 8000)  |  Frontend: Vite (Port 5173)"
echo "===================================================================="
echo -e "${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Xac dinh trinh thuc thi Python
if [ -f "$SCRIPT_DIR/backend/.venv/Scripts/python.exe" ]; then
    PYTHON_BIN="$SCRIPT_DIR/backend/.venv/Scripts/python.exe"
elif [ -f "$SCRIPT_DIR/backend/.venv/bin/python" ]; then
    PYTHON_BIN="$SCRIPT_DIR/backend/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo -e "${RED}[LOI] Khong tim thay Python tren he thong!${NC}"
    exit 1
fi

echo -e "${GREEN}[1/4] Su dung Python:${NC} $PYTHON_BIN"

# 2. Kiem tra thu vien Frontend
if [ ! -d "$SCRIPT_DIR/frontend/node_modules" ]; then
    echo -e "${YELLOW}[2/4] Thu muc node_modules chua ton tai, dang chay npm install...${NC}"
    (cd "$SCRIPT_DIR/frontend" && npm install)
else
    echo -e "${GREEN}[2/4] Thu vien Frontend da san sang.${NC}"
fi

# Ham don dep tien trinh khi nhan Ctrl+C
cleanup() {
    echo ""
    echo -e "${YELLOW}Dang tat toan bo dich vu TrafficSign AI...${NC}"
    if [ -n "$BACKEND_PID" ]; then
        kill "$BACKEND_PID" 2>/dev/null || true
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill "$FRONTEND_PID" 2>/dev/null || true
    fi
    # Giai phong cong phong truong hop process con
    if command -v powershell.exe >/dev/null 2>&1; then
        powershell.exe -Command "Get-NetTCPConnection -LocalPort 8000, 5173 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id \$_.OwningProcess -Force -ErrorAction SilentlyContinue }" >/dev/null 2>&1 || true
    fi
    echo -e "${GREEN}Da tat thanh cong tat ca dich vu. Hen gap lai!${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 3. Khoi dong Backend
echo -e "${GREEN}[3/4] Dang khoi dong Backend FastAPI tai http://127.0.0.1:8000...${NC}"
(
    cd "$SCRIPT_DIR/backend"
    "$PYTHON_BIN" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
) &
BACKEND_PID=$!

# 4. Khoi dong Frontend
echo -e "${GREEN}[4/4] Dang khoi dong Frontend Vite tai http://127.0.0.1:5173...${NC}"
(
    cd "$SCRIPT_DIR/frontend"
    npm run dev -- --host 127.0.0.1 --port 5173
) &
FRONTEND_PID=$!

# Cho 3 giay de server san sang va tu dong mo trinh duyet
sleep 3
echo ""
echo -e "${CYAN}===================================================================="
echo -e "                 HE THONG DANG CHAY ON DINH!"
echo -e "  * Giao dien Web         : ${GREEN}http://127.0.0.1:5173${CYAN}"
echo -e "  * Tra cuu danh muc bien : ${GREEN}http://127.0.0.1:5173/signs${CYAN}"
echo -e "  * Tai lieu API (Swagger): ${GREEN}http://127.0.0.1:8000/docs${CYAN}"
echo -e "===================================================================="
echo -e "${YELLOW}Nhan [Ctrl + C] bat ky luc nao de DUNG toan bo du an.${NC}"
echo ""

# Mo trinh duyet
if command -v explorer.exe >/dev/null 2>&1; then
    explorer.exe "http://127.0.0.1:5173" >/dev/null 2>&1 || true
elif command -v start >/dev/null 2>&1; then
    start "http://127.0.0.1:5173" >/dev/null 2>&1 || true
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://127.0.0.1:5173" >/dev/null 2>&1 || true
fi

# Giu terminal cho den khi nguoi dung nhan Ctrl+C
wait "$BACKEND_PID" "$FRONTEND_PID"
