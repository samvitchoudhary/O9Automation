@echo off
echo ============================================================
echo Starting O9 Test Automation Platform
echo ============================================================

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed
    exit /b 1
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Start Backend
echo.
echo ============================================================
echo Starting Backend (Port 8000)...
echo ============================================================
cd backend
if not exist ".env" (
    echo Warning: backend/.env file not found
    echo Create it with: ANTHROPIC_API_KEY=your_key_here
)
start "Backend" /MIN cmd /c "python run.py > ../logs/backend.log 2>&1"
cd ..
timeout /t 3 /nobreak >nul

REM Start Frontend
echo.
echo ============================================================
echo Starting Frontend (Port 5173)...
echo ============================================================
cd frontend
start "Frontend" /MIN cmd /c "npm run dev > ../logs/frontend.log 2>&1"
cd ..
timeout /t 3 /nobreak >nul

REM Start Mock O9
echo.
echo ============================================================
echo Starting Mock O9 Website (Port 3001)...
echo ============================================================
cd mock-o9-website
start "Mock O9" /MIN cmd /c "python serve.py > ../logs/mock-o9.log 2>&1"
cd ..

echo.
echo ============================================================
echo All services started successfully!
echo ============================================================
echo.
echo Access URLs:
echo   Frontend:  http://localhost:5173
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo   Mock O9:   http://localhost:3001
echo.
echo Check logs folder for service logs
echo Press any key to stop all services...
echo ============================================================
pause >nul

REM Kill all windows
taskkill /FI "WINDOWTITLE eq Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Mock O9*" /F >nul 2>&1

