@echo off
REM RakanGPT Quick Start Script for Windows
REM Run this to set up and start both the backend and frontend

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════╗
echo ║      RakanGPT - Quick Start Setup      ║
echo ╚════════════════════════════════════════╝
echo.

REM Check Python
echo ✓ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%
echo.

REM Check .NET
echo ✓ Checking .NET installation...
dotnet --version >nul 2>&1
if errorlevel 1 (
    echo ❌ .NET is not installed or not in PATH.
    echo Please install .NET 6.0 or higher from https://dotnet.microsoft.com
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('dotnet --version') do set DOTNET_VERSION=%%i
echo ✓ .NET found: %DOTNET_VERSION%
echo.

REM Check for .env file
echo ✓ Checking for .env file...
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    copy .env.example .env >nul
    echo 📝 Please edit .env and add your ANTHROPIC_API_KEY
    echo    Then run this script again.
    pause
    exit /b 1
) else (
    echo ✓ .env file found
)
echo.

REM Set up Python backend
echo 📦 Setting up Python backend...
if not exist venv (
    echo   Creating virtual environment...
    python -m venv venv
)

echo   Activating virtual environment...
call venv\Scripts\activate.bat

echo   Installing Python dependencies...
pip install -q -r requirements.txt

echo ✓ Python backend ready
echo.

REM Set up C# frontend
echo 📦 Setting up C# frontend...
echo   Restoring NuGet packages...
dotnet restore -q

echo   Building C# application...
dotnet build -q

echo ✓ C# frontend ready
echo.

echo ╔════════════════════════════════════════╗
echo ║         Setup Complete! 🎉             ║
echo ╚════════════════════════════════════════╝
echo.
echo To start RakanGPT:
echo.
echo 1. In Command Prompt 1 - Start the Python backend:
echo    venv\Scripts\activate.bat
echo    python backend.py
echo.
echo 2. In Command Prompt 2 - Start the C# frontend:
echo    dotnet run
echo.
echo Then follow the on-screen menu!
echo.
pause
