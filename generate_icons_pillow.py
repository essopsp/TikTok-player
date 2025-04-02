#!/usr/bin/env python3

import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library not found. Please install it with:")
    print("pip install Pillow")
    exit(1)

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

# Use the largest icon as the source
SOURCE_ICON = './icons/icon-512x512.png'

def generate_pwa_icons():
    """Generate all the icon sizes for the PWA using Pillow."""
    print("Generating PWA icons from existing icon...")
    
    # Check if source file exists
    if not os.path.exists(SOURCE_ICON):
        print(f"Error: Source icon {SOURCE_ICON} not found.")
        return
    
    # Create the icons directory if it doesn't exist
    Path('./icons').mkdir(exist_ok=True)
    
    # Open the source image
    try:
        source_img = Image.open(SOURCE_ICON)
    except Exception as e:
        print(f"Error opening source image: {e}")
        return
    
    # Generate each icon size
    for size in ICON_SIZES:
        output_file = f'./icons/icon-{size}x{size}.png'
        
        # Skip if the file already exists and has the right size
        if os.path.exists(output_file):
            try:
                existing_img = Image.open(output_file)
                if existing_img.width == size and existing_img.height == size:
                    print(f"Skipping {output_file} (already exists)")
                    continue
            except:
                pass  # If we can't open the existing file, regenerate it
        
        try:
            # Create a new resized image with proper quality
            resized_img = source_img.resize((size, size), Image.LANCZOS)
            resized_img.save(output_file, optimize=True)
            print(f"Generated {output_file}")
        except Exception as e:
            print(f"Error generating {output_file}: {e}")
    
    print("Icon generation complete!")

if __name__ == "__main__":
    generate_pwa_icons() 