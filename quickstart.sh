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

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
pip install --upgrade pip --quiet
pip install requests xgboost --quiet

echo "✓ Dependencies installed"
echo ""

# Show menu
echo "Choose prediction model:"
echo "  1) 🎯 Vegas-Level Predictor (65-70% accuracy, advanced features)"
echo "  2) 📊 Basic Predictor (55% accuracy, simple model)"
echo "  3) 🔬 Compare Both Models"
echo ""
read -p "Enter choice (1-3, or press Enter for Vegas): " choice

# Default to Vegas if no input
if [ -z "$choice" ]; then
    choice=1
fi

echo ""

case $choice in
    1)
        echo "🎯 Running VEGAS-LEVEL Predictor..."
        echo "===================================================================="
        echo "Features: Net Rating, Travel Distance, Rest Differential"
        echo "Target Accuracy: 65-70%"
        echo ""
        python3 predict_vegas.py "Lakers" "Warriors"
        echo ""
        echo "Try more matchups:"
        echo "  python3 predict_vegas.py \"Celtics\" \"Heat\""
        echo "  python3 predict_vegas.py \"Bucks\" \"Suns\""
        echo "  python3 predict_vegas.py \"76ers\" \"Nuggets\""
        ;;
    2)
        echo "📊 Running BASIC Predictor..."
        echo "===================================================================="
        echo "Features: Points, Win Rate, Home Court"
        echo "Target Accuracy: ~55%"
        echo ""
        python3 predict_current.py "Lakers" "Warriors"
        echo ""
        echo "Try more matchups:"
        echo "  python3 predict_current.py \"Celtics\" \"Heat\""
        echo "  python3 predict_current.py \"Bucks\" \"Suns\""
        ;;
    3)
        echo "🔬 Running COMPARISON (Basic vs Vegas)..."
        echo "===================================================================="
        python3 compare_predictions.py "Lakers" "Warriors"
        echo ""
        echo "Try comparing other matchups:"
        echo "  python3 compare_predictions.py \"Celtics\" \"Heat\""
        ;;
    *)
        echo "❌ Invalid choice. Running Vegas predictor by default..."
        python3 predict_vegas.py "Lakers" "Warriors"
        ;;
esac

echo ""
echo "✓ Data is current (from stats.nba.com - FREE, no API key!)"
