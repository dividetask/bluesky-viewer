#!/bin/bash
# Installation script for Bluesky Terminal Viewer
# This script creates a virtual environment to avoid system pip issues

set -e  # Exit on any error

echo "Installing Bluesky Terminal Viewer..."
echo

# Find an available Python 3 version
PYTHON=""
for version in python3.11 python3.10 python3.9 python3.8 python3; do
    if command -v "$version" &> /dev/null; then
        PYTHON="$version"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Error: No Python 3 installation found!"
    echo "Please install Python 3.7 or higher."
    exit 1
fi

echo "Using: $PYTHON ($($PYTHON --version))"
echo

# Check if venv exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    echo "Creating virtual environment..."
    $PYTHON -m venv venv --without-pip

    # Try to install pip using ensurepip
    echo "Bootstrapping pip..."
    if venv/bin/python3 -m ensurepip --upgrade 2>/dev/null; then
        echo "✓ pip installed via ensurepip"
    else
        echo "ensurepip not available, downloading pip installer..."
        # Download get-pip.py
        if command -v curl &> /dev/null; then
            curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        elif command -v wget &> /dev/null; then
            wget -q https://bootstrap.pypa.io/get-pip.py
        else
            echo "Error: Neither curl nor wget is available to download pip."
            echo "Please install curl or wget, or install python3-pip manually."
            exit 1
        fi

        echo "Installing pip..."
        venv/bin/python3 get-pip.py
        rm get-pip.py
        echo "✓ pip installed"
    fi
fi

echo "Upgrading pip and installing dependencies..."
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
