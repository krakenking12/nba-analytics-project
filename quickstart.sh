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

# Load API key
if [ -f .env ]; then
    source load_env.sh
else
    echo "⚠️  No .env file found. API key required for real data."
    echo "   Running demo with SAMPLE DATA instead..."
    echo ""
    python3 demo.py
    echo ""
    echo "⚠️  This was SAMPLE DATA, not real NBA stats!"
    echo ""
    echo "To use REAL data:"
    echo "  1. Add your API key: echo 'NBA_API_KEY=your_key' > .env"
    echo "  2. Run: source load_env.sh && python3 predict_matchup.py"
    exit 0
fi

# Run real prediction
echo "🚀 Running NBA Matchup Predictor with REAL 2025-2026 Season Data..."
echo "=================================================================="
echo ""
python3 predict_matchup.py "Lakers" "Warriors"

echo ""
echo "✅ Prediction complete using REAL NBA data!"
echo ""
echo "Try more matchups:"
echo "  python3 predict_matchup.py \"Celtics\" \"Heat\""
echo "  python3 predict_matchup.py \"Bucks\" \"Suns\""
echo "  python3 predict_matchup.py  # Interactive mode"
