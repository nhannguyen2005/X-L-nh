#!/usr/bin/env bash

# ====================================================================
#               TRAFFICSIGN AI - SCRIPT DUNG DICH VU (BASH)
# ====================================================================

echo "Dang giai phong cac cong 8000 (Backend) va 5173 (Frontend)..."

if command -v powershell.exe >/dev/null 2>&1; then
    powershell.exe -Command "Get-NetTCPConnection -LocalPort 8000, 5173 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id \$_.OwningProcess -Force -ErrorAction SilentlyContinue }" >/dev/null 2>&1 || true
else
    # Linux / macOS fallback
    lsof -ti:8000,5173 | xargs kill -9 2>/dev/null || true
fi

echo "Da tat toan bo dich vu TrafficSign AI thanh cong!"
