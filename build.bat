@echo off
echo Building ReelDownloader...

REM Clean previous builds
rmdir /s /q build
rmdir /s /q dist

REM Run PyInstaller
python -m PyInstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --icon "icon.ico" ^
    --name "ReelDownloader" ^
    --add-data "fonts;fonts" ^
    --add-data "icon.ico;." ^
    "main.py"

echo Build complete! Check the 'dist\ReelDownloader' folder.
pause
