#!/bin/bash
# Quick start script for running the tutorial locally

set -e

echo "=================================="
echo "Python for Engineers - Quick Start"
echo "=================================="
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo

# Check if dependencies are installed
if ! pip show flask > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
    echo
else
    echo "✓ Dependencies already installed"
    echo
fi

# Display instructions
echo "=================================="
echo "Ready to run!"
echo "=================================="
echo
echo "To run the map server:"
echo "  python src/map_server/app.py"
echo
echo "To run the agent (in another terminal):"
echo "  source venv/bin/activate"
echo "  python src/agent/main.py"
echo
echo "=================================="
echo

# Ask what to run
echo "What would you like to run?"
echo "  1) Map Server"
echo "  2) Agent (requires map server running)"
echo "  3) Exit"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo
        echo "Starting Map Server..."
        echo "Press CTRL+C to stop"
        echo
        python src/map_server/app.py
        ;;
    2)
        echo
        echo "Starting Agent..."
        echo "Make sure the map server is running in another terminal!"
        echo
        sleep 2
        python src/agent/main.py
        ;;
    3)
        echo "Goodbye!"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
