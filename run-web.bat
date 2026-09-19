@echo off
REM RakanGPT Web Version - Quick Start for Windows
REM Runs the Flask web application

cls
echo.
echo ╔════════════════════════════════════════╗
echo ║     RakanGPT - Web Application         ║
echo ╚════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo.
    echo ⚠️  .env file not found!
    echo Please create .env with your API key:
    echo.
    echo   copy .env.example .env
    echo   Edit .env and add your ANTHROPIC_API_KEY
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ Setup complete!
echo.
echo ╔════════════════════════════════════════╗
echo ║    Starting RakanGPT Web Server        ║
echo ╚════════════════════════════════════════╝
echo.
echo 🌐 Access the app at: http://localhost:5000
echo 📚 Stop with: Ctrl+C
echo.

REM Run the Flask app
python app.py
pause
