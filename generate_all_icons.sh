#!/bin/bash

# Script to generate all icons for the TikTok Player PWA

echo "=== TikTok Player PWA Icon Generator ==="
echo ""

# Check for Python
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Error: Python not found. Please install Python 3."
    exit 1
fi

# Check for Pillow
$PYTHON -c "import PIL" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing Pillow library..."
    $PYTHON -m pip install Pillow
fi

# Create directories
mkdir -p ./icons/material

# Step 1: Generate PNG icons from existing 512x512 icon
echo "Generating PNG icons in various sizes..."
$PYTHON ./generate_icons_pillow.py

# Step 2: Download Material Icons for offline use
echo "Downloading Material Icons for offline use..."
$PYTHON ./download_material_icons.py

# Step 3: Generate SVG to PNG conversions (helper script)
echo "Generating SVG icons..."
$PYTHON ./generate_svgs_to_pngs.py

echo ""
echo "Icon generation complete!"
echo "Please verify that all required icons were created successfully."
echo "If any icons are missing, you may need to convert them manually using the provided SVG files."
echo "See the instructions in generate_svgs_to_pngs.py for more details."
echo ""
echo "Don't forget to update your manifest.json if you've added new icon sizes."
echo ""
echo "=== Done ===" 