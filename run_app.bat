@echo off

REM AAS Risk Reduction Tool - Launch Script for Windows
REM This script sets up the environment and runs the application

echo 🚀 AAS Risk Reduction Tool - Starting Application
echo ==================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment found
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt >nul 2>&1

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
) else (
    echo ✅ Dependencies installed successfully
)

REM Run tests
echo 🧪 Running application tests...
python test_app.py >nul 2>&1

if errorlevel 1 (
    echo ⚠️  Some tests failed, but continuing...
) else (
    echo ✅ All tests passed
)

REM Start the application
echo 🌐 Starting Streamlit application...
echo 📍 The application will open at: http://localhost:8501
echo 💡 Press Ctrl+C to stop the application
echo.

REM Launch Streamlit
streamlit run app.py

echo.
echo 👋 Application stopped. Thank you for using AAS Risk Reduction Tool!
pause