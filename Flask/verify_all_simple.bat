@echo off
setlocal enabledelayedexpansion

echo.
echo =======================================================
echo ==    Walmart Secure Backend Verification Script     ==
echo =======================================================
echo.

set "API_URL=http://localhost:8000/api"
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
for /f "delims=" %%i in ('curl -s -X POST -H "Content-Type: application/json" -d "{\"email\":\"%TEST_EMAIL%\",\"password\":\"%TEST_PASSWORD%\"}" %API_URL%/login') do set LOGIN_RESPONSE=%%i
echo Login Response: !LOGIN_RESPONSE!

REM Extract token using PowerShell
for /f "delims=" %%i in ('powershell -Command "try { $response = '%LOGIN_RESPONSE%'; $data = $response ^| ConvertFrom-Json; if ($data.access_token) { $data.access_token } else { 'NO_TOKEN_FOUND' } } catch { 'NO_TOKEN_FOUND' }"') do set USER_TOKEN=%%i

if "%USER_TOKEN%"=="NO_TOKEN_FOUND" (
    echo ERROR: Could not get user token. Aborting.
    goto :eof
)
echo User Token Captured Successfully: %USER_TOKEN:~0,20%...
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
for /f "delims=" %%i in ('curl -s -X POST -H "Content-Type: application/json" -d "{\"email\":\"%ADMIN_EMAIL%\",\"password\":\"%ADMIN_PASSWORD%\"}" %API_URL%/login') do set ADMIN_LOGIN_RESPONSE=%%i
echo Admin Login Response: !ADMIN_LOGIN_RESPONSE!

REM Extract admin token using PowerShell
for /f "delims=" %%i in ('powershell -Command "try { $response = '%ADMIN_LOGIN_RESPONSE%'; $data = $response ^| ConvertFrom-Json; if ($data.access_token) { $data.access_token } else { 'NO_TOKEN_FOUND' } } catch { 'NO_TOKEN_FOUND' }"') do set ADMIN_TOKEN=%%i

if "%ADMIN_TOKEN%"=="NO_TOKEN_FOUND" (
    echo ERROR: Could not get admin token. Aborting.
    goto :eof
)
echo Admin Token Captured Successfully: %ADMIN_TOKEN:~0,20%...
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