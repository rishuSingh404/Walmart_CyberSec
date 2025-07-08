@echo off
echo Starting Walmart CyberSec Application...
echo.

echo [1/2] Starting Flask Backend API...
cd /d "%~dp0\flask"
start "Flask Backend" cmd /k "start_flask.bat"

echo [2/2] Starting React Frontend...
cd /d "%~dp0"
timeout /t 3 /nobreak >nul
start "React Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo Walmart CyberSec Application Started!
echo ========================================
echo Flask API: http://localhost:5001
echo React App: http://localhost:5173
echo.
echo Press any key to continue...
pause >nul
