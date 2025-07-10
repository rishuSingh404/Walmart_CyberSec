@echo off
echo Starting Walmart Cybersecurity Demo...

echo Creating virtual environment if it doesn't exist...
if not exist venv (
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r backend\requirements.txt

echo Starting backend server in a new window...
start cmd /k "call venv\Scripts\activate.bat && python -m backend.app"

echo Installing frontend dependencies...
cd frontend
npm install

echo Starting frontend development server...
npm run dev

echo All services started successfully! 