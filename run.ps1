# ====================================================================
#               TRAFFICSIGN AI - POWERSHELL LAUNCHER
#       He thong Nhan dien & Tra cuu Bien bao Giao thong Viet Nam
# ====================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "TrafficSign AI - System Launcher"

Write-Host ""
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "               TRAFFICSIGN AI - KHOI DONG TOAN BO HE THONG" -ForegroundColor Cyan
Write-Host "       Backend: FastAPI (Port 8000)  |  Frontend: Vite (Port 5173)" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RootDir

# 1. Kiem tra Python
$PythonExe = Join-Path $RootDir "backend\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "[CANH BAO] Khong tim thay backend\.venv. Su dung python he thong..." -ForegroundColor Yellow
    $PythonExe = "python"
} else {
    Write-Host "[1/3] Su dung Python ao: $PythonExe" -ForegroundColor Green
}

# 2. Kiem tra Frontend
$NodeModules = Join-Path $RootDir "frontend\node_modules"
if (-not (Test-Path $NodeModules)) {
    Write-Host "[THONG BAO] Dang cai dat thu vien Frontend (npm install)..." -ForegroundColor Yellow
    Set-Location (Join-Path $RootDir "frontend")
    npm install
    Set-Location $RootDir
}

# 3. Khoi dong Backend
Write-Host "[2/3] Dang khoi dong Backend FastAPI tai http://127.0.0.1:8000..." -ForegroundColor Green
$BackendDir = Join-Path $RootDir "backend"
Start-Process cmd.exe -ArgumentList "/k cd /d `"$BackendDir`" && `"$PythonExe`" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

# 4. Khoi dong Frontend
Write-Host "[3/3] Dang khoi dong Frontend Vite tai http://127.0.0.1:5173..." -ForegroundColor Green
$FrontendDir = Join-Path $RootDir "frontend"
Start-Process cmd.exe -ArgumentList "/k cd /d `"$FrontendDir`" && npm run dev -- --host 127.0.0.1 --port 5173"

# 5. Cho 4 giay va mo trinh duyet
Write-Host "Cho he thong san sang..." -ForegroundColor Yellow
Start-Sleep -Seconds 4
Start-Process "http://127.0.0.1:5173"

Write-Host ""
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "                  HE THONG DA SAN SANG PHUC VU!" -ForegroundColor Green
Write-Host "  * Giao dien Web         : http://127.0.0.1:5173" -ForegroundColor White
Write-Host "  * Tra cuu 65 bien bao   : http://127.0.0.1:5173/signs" -ForegroundColor White
Write-Host "  * Tai lieu API (Swagger): http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""
