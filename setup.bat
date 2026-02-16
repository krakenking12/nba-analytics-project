@echo off
REM NBA Analytics Project - Quick Setup Script (Windows)
REM Run this after downloading the project

echo ============================================
echo NBA Analytics Project - Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed.
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo + Python found
python --version
echo.

REM Install dependencies
set /p install="Install required packages? (y/n): "
if /i "%install%"=="y" (
    echo Installing packages...
    pip install -r requirements.txt
    echo + Packages installed
) else (
    echo Skipping package installation
    echo Note: You can run demo.py without packages
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To run the demo (no internet needed):
echo   python demo.py
echo.
echo To run the full version (requires internet):
echo   python nba_analytics.py
echo.
pause
