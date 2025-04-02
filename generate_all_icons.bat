@echo off
echo === TikTok Player PWA Icon Generator ===
echo.

REM Check for Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found. Please install Python 3.
    exit /b 1
)

REM Check for Pillow
python -c "import PIL" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Pillow library...
    python -m pip install Pillow
)

REM Create directories
if not exist ".\icons\material" mkdir ".\icons\material"

REM Step 1: Generate PNG icons from existing 512x512 icon
echo Generating PNG icons in various sizes...
python .\generate_icons_pillow.py

REM Step 2: Download Material Icons for offline use
echo Downloading Material Icons for offline use...
python .\download_material_icons.py

REM Step 3: Generate SVG to PNG conversions (helper script)
echo Generating SVG icons...
python .\generate_svgs_to_pngs.py

echo.
echo Icon generation complete!
echo Please verify that all required icons were created successfully.
echo If any icons are missing, you may need to convert them manually using the provided SVG files.
echo See the instructions in generate_svgs_to_pngs.py for more details.
echo.
echo Don't forget to update your manifest.json if you've added new icon sizes.
echo.
echo === Done ===

pause 