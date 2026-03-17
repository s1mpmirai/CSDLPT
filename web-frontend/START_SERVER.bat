@echo off
REM Simple HTTP Server launcher for HR Payroll Web Frontend
REM This will start Python HTTP server on port 8000

echo.
echo ========================================
echo HR PAYROLL Web Frontend Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found!
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo Starting web server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
echo Make sure Flask backend is running on http://localhost:5000
echo.

REM Start HTTP server
python -m http.server 8000

pause
