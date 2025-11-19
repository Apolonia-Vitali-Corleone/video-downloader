#!/bin/bash

# Video Downloader Launcher Script for Mac/Linux

echo "Starting Video Downloader..."

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "Using virtual environment..."
    # Activate virtual environment
    source .venv/bin/activate
    python app.py
else
    echo "Virtual environment not found, running with system Python..."
    python3 app.py
fi
