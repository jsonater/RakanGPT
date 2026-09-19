#!/bin/bash

# RakanGPT Web Version - Quick Start
# Runs the Flask web application

echo "╔════════════════════════════════════════╗"
echo "║     RakanGPT - Web Application         ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "Please create .env with your API key:"
    echo ""
    echo "  cp .env.example .env"
    echo "  nano .env  # Add your ANTHROPIC_API_KEY"
    echo ""
    exit 1
fi

# Check API key
if ! grep -q "ANTHROPIC_API_KEY" .env; then
    echo "❌ ANTHROPIC_API_KEY not found in .env"
    exit 1
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "╔════════════════════════════════════════╗"
echo "║    Starting RakanGPT Web Server        ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "🌐 Access the app at: http://localhost:5000"
echo "📚 Stop with: Ctrl+C"
echo ""

# Open the browser automatically when running in a desktop environment
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:5000" >/dev/null 2>&1 &
elif command -v open >/dev/null 2>&1; then
    open "http://localhost:5000" >/dev/null 2>&1 &
fi

# Run the Flask app
python app.py
