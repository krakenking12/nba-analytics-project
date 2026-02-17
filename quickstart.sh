#!/bin/bash
# NBA Analytics Project - Quick Start Script
# Uses CURRENT data from stats.nba.com (no API key needed!)

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

# Install only requests (lightweight, no architecture issues)
echo ""
echo "📚 Installing dependencies (requests only)..."
pip install --upgrade pip --quiet
pip install requests --quiet

echo "✓ Dependencies installed"
echo ""

# Run prediction with CURRENT data
echo "🚀 Running NBA Matchup Predictor with CURRENT 2025-26 Season Data..."
echo "===================================================================="
echo "📊 Using stats.nba.com (FREE, no API key required!)"
echo ""
python3 predict_current.py "Lakers" "Warriors"

echo ""
echo "✅ Prediction complete using CURRENT NBA data!"
echo ""
echo "Try more matchups:"
echo "  python3 predict_current.py \"Celtics\" \"Heat\""
echo "  python3 predict_current.py \"Bucks\" \"Suns\""
echo "  python3 predict_current.py \"76ers\" \"Nuggets\""
echo ""
echo "✓ Data is only 4 days old (not 105 days like the old API!)"
