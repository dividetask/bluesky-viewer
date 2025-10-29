#!/bin/bash
# Installation script for Bluesky Terminal Viewer
# This script works around broken pip3 installations

echo "Installing dependencies for Bluesky Terminal Viewer..."
echo

# Use python3 -m pip instead of pip3 to avoid system pip issues
python3 -m pip install -r requirements.txt --user

if [ $? -eq 0 ]; then
    echo
    echo "✓ Installation successful!"
    echo
    echo "You can now run the viewer with:"
    echo "  python3 main.py"
    echo
else
    echo
    echo "✗ Installation failed. Please check the error messages above."
    exit 1
fi
