#!/bin/bash
# Run script for Bluesky Terminal Viewer
# Automatically uses the virtual environment

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running installation..."
    ./install.sh
fi

# Run the viewer using the venv python
venv/bin/python3 main.py "$@"
