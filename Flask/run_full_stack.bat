@echo off
setlocal

echo Starting Walmart Secure Backend...
start cmd /k "cd /d "%~dp0" && .\rebuild_and_run.bat"

echo Waiting for backend to start (adjust as needed)...
timeout /t 10 /nobreak >nul

echo Starting Next.js Frontend Development Server...
rem Make sure you are in the correct frontend directory for this command.
cd /d "%~dp0frontend"
call npm run dev

endlocal
pause