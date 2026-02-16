#!/bin/bash
# NBA Analytics Project - Quick Setup Script
# Run this after downloading the project

echo "============================================"
echo "NBA Analytics Project - Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed."
    echo "Please install pip3"
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install dependencies (optional - only needed for full version)
read -p "Install required packages? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing packages..."
    pip3 install -r requirements.txt
    echo "✓ Packages installed"
else
    echo "Skipping package installation"
    echo "Note: You can run demo.py without packages"
fi

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "To run the demo (no internet needed):"
echo "  python3 demo.py"
echo ""
echo "To run the full version (requires internet):"
echo "  python3 nba_analytics.py"
echo ""
