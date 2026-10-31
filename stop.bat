@echo off
chcp 65001 >nul
title Dung TrafficSign AI
color 0C

echo.
echo ====================================================================
echo               TRAFFICSIGN AI - DUNG TOAN BO HE THONG
echo ====================================================================
echo.
echo Dang giai phong cac cong 8000 (Backend) va 5173 (Frontend)...

powershell -Command ^
  "$ports = @(8000, 5173); " ^
  "foreach ($p in $ports) { " ^
  "  $conns = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue; " ^
  "  if ($conns) { " ^
  "    $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique; " ^
  "    foreach ($procId in $pids) { " ^
  "      try { Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue; Write-Host '  [OK] Da dung tien trinh PID:' $procId 'tren cong' $p } catch {} " ^
  "    } " ^
  "  } else { Write-Host '  [-] Cong' $p 'da trong.' } " ^
  "}"

echo.
echo ====================================================================
echo            DA DUNG TOAN BO DICH VU TRAFFICSIGN AI!
echo ====================================================================
echo.
timeout /t 3
