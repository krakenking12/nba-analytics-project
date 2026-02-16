@echo off
REM NBA Analytics Project - Quick Start Script (Windows)
REM This script sets up a virtual environment and runs a simple demo

echo.
echo 🏀 NBA Analytics Project - Quick Start
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo 📚 Installing dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo ✓ Dependencies installed
echo.

REM Run the demo
echo 🚀 Running NBA Analytics Demo...
echo ================================
echo.
python demo.py

echo.
echo ✅ Demo complete!
echo.
echo Next steps:
echo   1. Check the generated 'nba_analytics_dashboard.png' for visualizations
echo   2. Run 'python nba_analytics.py' for the full analysis
echo   3. Modify the code to explore different teams or seasons
echo.
pause
