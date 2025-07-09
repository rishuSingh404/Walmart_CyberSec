@echo off
setlocal

echo.
echo =======================================================
echo ==    Walmart Secure Backend Verification Script     ==
echo =======================================================
echo.

set "API_URL=http://localhost:8000/api"
set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
set "UNIQUE_ID=%RANDOM%"
set "TEST_EMAIL=testuser_%UNIQUE_ID%@example.com"
set "TEST_PASSWORD=StrongPassword123"
set "ADMIN_EMAIL=admin@walmart.com"
set "ADMIN_PASSWORD=AdminPassword123"

echo --- Step 1: Health Check ---
curl %API_URL%/../
echo.
echo.

echo --- Step 2: User Signup (Email: %TEST_EMAIL%) ---
curl -X POST -H "Content-Type: application/json" -d "{\"email\":\"%TEST_EMAIL%\",\"password\":\"%TEST_PASSWORD%\"}" %API_URL%/signup
echo.
echo.

echo --- Step 3: User Login and Token Capture ---
for /f "delims=" %%i in ('curl -s -X POST -H "Content-Type: application/json" -d "{\"email\":\"%TEST_EMAIL%\",\"password\":\"%TEST_PASSWORD%\"}" %API_URL%/login ^| "%PYTHON_EXE%" backend/_get_token.py') do set USER_TOKEN=%%i
if "%USER_TOKEN%"=="NO_TOKEN_FOUND" (
    echo ERROR: Could not get user token. Aborting.
    goto :eof
)
echo User Token Captured Successfully.
echo.

echo --- Step 4: Fingerprint Update (Protected) ---
curl -H "Authorization: Bearer %USER_TOKEN%" -X POST -H "Content-Type: application/json" -d "{\"typing_speed\":120, \"click_count\":15}" %API_URL%/fingerprint/update
echo.
echo.

echo --- Step 5: Risk Assessment (Protected) ---
curl -H "Authorization: Bearer %USER_TOKEN%" -X POST -H "Content-Type: application/json" -d "{\"typing_speed\": 100, \"mouse_distance\": 500}" %API_URL%/risk/assess
echo.
echo.

echo --- Step 6: Admin Login and Token Capture ---
for /f "delims=" %%i in ('curl -s -X POST -H "Content-Type: application/json" -d "{\"email\":\"%ADMIN_EMAIL%\",\"password\":\"%ADMIN_PASSWORD%\"}" %API_URL%/login ^| "%PYTHON_EXE%" backend/_get_token.py') do set ADMIN_TOKEN=%%i
if "%ADMIN_TOKEN%"=="NO_TOKEN_FOUND" (
    echo ERROR: Could not get admin token. Aborting.
    goto :eof
)
echo Admin Token Captured Successfully.
echo.

echo --- Step 7: Admin Users Endpoint (Admin-Only) ---
curl -H "Authorization: Bearer %ADMIN_TOKEN%" %API_URL%/admin/users
echo.
echo.

echo --- Step 8: Analytics Dashboard Endpoint (Admin-Only) ---
curl -H "Authorization: Bearer %ADMIN_TOKEN%" %API_URL%/analytics/dashboard
echo.
echo.

echo =======================================================
echo ==              Verification Complete                ==
echo =======================================================
echo.

endlocal
pause 