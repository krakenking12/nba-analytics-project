#!/bin/bash
# NBA Analytics Project - Quick Start Script
# This script sets up a virtual environment and runs a simple demo

echo "🏀 NBA Analytics Project - Quick Start"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo "✓ Dependencies installed"
echo ""

# Run the demo
echo "🚀 Running NBA Analytics Demo..."
echo "================================"
echo ""
python3 demo.py

echo ""
echo "✅ Demo complete!"
echo ""
echo "Next steps:"
echo "  1. Check the generated 'nba_analytics_dashboard.png' for visualizations"
echo "  2. Run 'python3 nba_analytics.py' for the full analysis"
echo "  3. Modify the code to explore different teams or seasons"
echo ""
echo "To run again: source venv/bin/activate && python3 demo.py"
