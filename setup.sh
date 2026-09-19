#!/bin/bash

# RakanGPT Quick Start Script
# Run this to set up and start both the backend and frontend

echo "╔════════════════════════════════════════╗"
echo "║      RakanGPT - Quick Start Setup      ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check .NET
echo "✓ Checking .NET installation..."
if ! command -v dotnet &> /dev/null; then
    echo "❌ .NET is not installed. Please install .NET 6.0 or higher."
    exit 1
fi
echo "✓ .NET found: $(dotnet --version)"
echo ""

# Check for .env file
echo "✓ Checking for .env file..."
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your ANTHROPIC_API_KEY"
    echo "   Then run this script again."
    exit 1
else
    echo "✓ .env file found"
fi
echo ""

# Set up Python backend
echo "📦 Setting up Python backend..."
if [ ! -d venv ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

echo "  Activating virtual environment..."
source venv/bin/activate

echo "  Installing Python dependencies..."
pip install -q -r requirements.txt

echo "✓ Python backend ready"
echo ""

# Set up C# frontend
echo "📦 Setting up C# frontend..."
echo "  Restoring NuGet packages..."
dotnet restore -q

echo "  Building C# application..."
dotnet build -q

echo "✓ C# frontend ready"
echo ""

echo "╔════════════════════════════════════════╗"
echo "║         Setup Complete! 🎉             ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "To start RakanGPT:"
echo ""
echo "1. In Terminal 1 - Start the Python backend:"
echo "   source venv/bin/activate"
echo "   python backend.py"
echo ""
echo "2. In Terminal 2 - Start the C# frontend:"
echo "   dotnet run"
echo ""
echo "Then follow the on-screen menu!"
echo ""
