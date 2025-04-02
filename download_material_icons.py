#!/usr/bin/env python3

import os
import json
import urllib.request
from pathlib import Path

# List of Material Icons used in the app
ICONS = [
    "link",
    "close",
    "play_arrow",
    "download",
    "movie",
    "fullscreen",
    "history",
    "play_circle_filled",
    "sync",
    "signal_wifi_off",
    "error"
]

# Material icons URL template
ICON_URL_TEMPLATE = "https://fonts.gstatic.com/s/i/materialicons/{icon_name}/v1/24px.svg"

def download_material_icons():
    """Download Material Icons and save them locally."""
    print("Downloading Material Icons...")
    
    # Create the directory for material icons
    icons_dir = Path('./icons/material')
    icons_dir.mkdir(exist_ok=True, parents=True)
    
    # Create a CSS file to map the icons
    css_content = """
/* Material Icons Local Fallback */
@font-face {
  font-family: 'Material Icons Local';
  font-style: normal;
  font-weight: 400;
  src: local('Material Icons'),
       local('MaterialIcons-Regular');
}

.material-icons-local {
  font-family: 'Material Icons Local';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}
"""
    
    # Create a JS file to map the icons for offline use
    js_content = """
// Material Icons Offline Fallback
(function() {
  // Check if online to decide whether to use CDN or local icons
  const isOnline = navigator.onLine;
  if (isOnline) {
    return; // Use the CDN if online
  }
  
  // Create a mapping of icon names to SVG content
  const iconMap = {
"""
    
    # Download each icon
    for icon_name in ICONS:
        url = ICON_URL_TEMPLATE.format(icon_name=icon_name)
        output_file = icons_dir / f"{icon_name}.svg"
        
        try:
            print(f"Downloading {icon_name} icon...")
            response = urllib.request.urlopen(url)
            svg_content = response.read().decode('utf-8')
            
            # Write the SVG file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            # Add to the JS content
            js_content += f"    '{icon_name}': `{svg_content}`,\n"
            
            print(f"Saved {output_file}")
        except Exception as e:
            print(f"Error downloading {icon_name}: {e}")
    
    # Finish and save the JS file
    js_content += """  };
  
  // Create a function to replace icons with SVG when needed
  function replaceIconsWithSvg() {
    const icons = document.querySelectorAll('.material-icons');
    icons.forEach(icon => {
      const iconName = icon.textContent.trim();
      if (iconMap[iconName]) {
        const svgContainer = document.createElement('span');
        svgContainer.innerHTML = iconMap[iconName];
        svgContainer.className = 'material-icons-svg';
        svgContainer.style.display = 'inline-block';
        svgContainer.style.width = '24px';
        svgContainer.style.height = '24px';
        svgContainer.style.verticalAlign = 'middle';
        icon.parentNode.replaceChild(svgContainer, icon);
      }
    });
  }
  
  // Run on page load and when new elements might be added
  document.addEventListener('DOMContentLoaded', replaceIconsWithSvg);
  
  // Create an observer to look for new icons
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.addedNodes.length) {
        replaceIconsWithSvg();
      }
    });
  });
  
  // Start observing when the page is loaded
  document.addEventListener('DOMContentLoaded', () => {
    observer.observe(document.body, { childList: true, subtree: true });
  });
})();
"""
    
    # Save the JS file
    js_file = Path('./icons/material-icons-fallback.js')
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Material Icons downloaded successfully!")
    print(f"Use the fallback script by adding this to your HTML:")
    print(f'<script src="./icons/material-icons-fallback.js"></script>')

if __name__ == "__main__":
    download_material_icons() 