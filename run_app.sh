#!/bin/bash

# AAS Risk Reduction Tool - Launch Script
# This script sets up the environment and runs the application

echo "🚀 AAS Risk Reduction Tool - Starting Application"
echo "=================================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if (( $(echo "$python_version < $required_version" | bc -l) )); then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run tests
echo "🧪 Running application tests..."
python test_app.py > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ All tests passed"
else
    echo "⚠️  Some tests failed, but continuing..."
fi

# Start the application
echo "🌐 Starting Streamlit application..."
echo "📍 The application will open at: http://localhost:8501"
echo "💡 Press Ctrl+C to stop the application"
echo ""

# Launch Streamlit
streamlit run app.py

echo ""
echo "👋 Application stopped. Thank you for using AAS Risk Reduction Tool!"