#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

# List of icon sizes needed for a complete PWA
ICON_SIZES = [
    48,
    72,
    96, 
    120,  # iOS
    128,
    144,
    152,  # iOS
    180,  # iOS
    192,
    256,
    384,
    512
]

# Source SVG file
SVG_SOURCE = './icons/tiktok-logo/tiktok-logo.svg'

def generate_pwa_icons():
    """Generate all the icon sizes for the PWA."""
    print("Generating PWA icons from SVG...")
    
    # Create the icons directory if it doesn't exist
    Path('./icons').mkdir(exist_ok=True)
    
    # Check if Inkscape is available (for SVG to PNG conversion)
    inkscape_available = False
    try:
        result = subprocess.run(['inkscape', '--version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        inkscape_available = result.returncode == 0
    except FileNotFoundError:
        print("Inkscape not found. Will use ImageMagick's convert if available.")
    
    # Check if ImageMagick is available
    imagemagick_available = False
    try:
        result = subprocess.run(['convert', '--version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        imagemagick_available = result.returncode == 0
    except FileNotFoundError:
        print("ImageMagick not found.")
    
    if not inkscape_available and not imagemagick_available:
        print("Neither Inkscape nor ImageMagick found. Cannot convert SVG to PNG.")
        print("Please install one of these tools or manually convert the SVG to PNG icons.")
        return
    
    # Generate each icon size
    for size in ICON_SIZES:
        output_file = f'./icons/icon-{size}x{size}.png'
        
        if inkscape_available:
            try:
                cmd = [
                    'inkscape',
                    '--export-filename', output_file,
                    '--export-width', str(size),
                    '--export-height', str(size),
                    SVG_SOURCE
                ]
                subprocess.run(cmd, check=True)
                print(f"Generated {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error generating {output_file}: {e}")
        elif imagemagick_available:
            try:
                cmd = [
                    'convert',
                    '-background', 'none',
                    '-size', f'{size}x{size}',
                    SVG_SOURCE,
                    '-resize', f'{size}x{size}',
                    output_file
                ]
                subprocess.run(cmd, check=True)
                print(f"Generated {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error generating {output_file}: {e}")

    print("Icon generation complete!")
    print("If you don't have Inkscape or ImageMagick installed,")
    print("you'll need to manually convert the SVG to PNG icons of the required sizes.")

if __name__ == "__main__":
    generate_pwa_icons() 