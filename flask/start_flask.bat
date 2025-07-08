@echo off
echo Starting Flask adapter service...
cd %~dp0
echo Working directory: %CD%

REM Activate the virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Set environment variables
set BACKEND_URL=http://localhost:8000
set MODEL_API_URL=http://localhost:5000

echo Starting Flask application...
python app.py

pause 