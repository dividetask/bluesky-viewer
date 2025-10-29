#!/bin/bash
# Installation script for Bluesky Terminal Viewer
# This script creates a virtual environment to avoid system pip issues

set -e  # Exit on any error

echo "Installing Bluesky Terminal Viewer..."
echo

# Check if venv exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    echo "Creating virtual environment..."
    python3.11 -m venv venv --without-pip

    # Manually install pip in the venv using ensurepip
    echo "Bootstrapping pip..."
    venv/bin/python3 -m ensurepip --upgrade
fi

echo "Installing dependencies..."
venv/bin/python3 -m pip install --upgrade pip setuptools wheel
venv/bin/python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "✓ Installation successful!"
    echo
    echo "To run the viewer, use:"
    echo "  ./run.sh"
    echo
    echo "Or activate the virtual environment:"
    echo "  source venv/bin/activate"
    echo "  python3 main.py"
    echo
else
    echo
    echo "✗ Installation failed."
    exit 1
fi
