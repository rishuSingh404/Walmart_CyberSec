@echo off
setlocal

echo ========================================================
echo ==  Rebuilding Environment and Starting Backend       ==
echo ========================================================
echo.

REM --- Environment Reconstruction ---
if exist venv (
    echo Deleting existing virtual environment...
    rmdir /s /q venv
)

echo Creating new virtual environment...
python -m venv venv
echo.

REM Get the directory of the batch file
set "BATCH_DIR=%~dp0"

REM --- Absolute paths to executables ---
set "PYTHON_EXE=%BATCH_DIR%venv\Scripts\python.exe"
set "PIP_EXE=%BATCH_DIR%venv\Scripts\pip.exe"

REM --- Dependency Installation ---
echo Installing/Verifying dependencies with absolute path...
"%PIP_EXE%" install -r "%BATCH_DIR%backend\requirements.txt"
if %errorlevel% neq 0 (
    echo.
    echo *******************************************************
    echo **   ERROR: Dependency installation failed. Aborting.  **
    echo *******************************************************
    pause
    exit /b
)


REM --- Database and Admin Creation ---
echo Creating database and admin user with absolute path...
"%PYTHON_EXE%" "%BATCH_DIR%backend\create_admin.py" --email admin@walmart.com --password AdminPassword123
if %errorlevel% neq 0 (
    echo.
    echo *******************************************************
    echo **   ERROR: Admin creation failed. Aborting.         **
    echo *******************************************************
    pause
    exit /b
)

REM --- Application Launch ---
echo Launching Flask application from the root with absolute path...
echo Your application will be available at http://localhost:8000
set "FLASK_APP=backend.app"
"%PYTHON_EXE%" -m flask run --host=0.0.0.0 --port=8000

endlocal
pause 