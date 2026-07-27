@echo off
REM ============================================================
REM   RigDeck - one-click EXE builder (Windows)
REM ============================================================
title RigDeck - EXE Builder
cd /d "%~dp0"
echo.
echo  ============================================================
echo    RIGDECK  -  EXE BUILDER
echo  ============================================================
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo  [X] Python was not found on this PC.
    echo      Install Python 3 from https://www.python.org/downloads/
    echo      IMPORTANT: tick "Add python.exe to PATH" on the first screen.
    pause
    exit /b 1
)
echo  [OK] Python found:
python --version
echo.
echo  [..] Installing build tool and dependencies (first run only)...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install pyinstaller flask truck-telemetry pydirectinput
if errorlevel 1 (
    echo  [X] Package install failed - check your internet connection.
    pause
    exit /b 1
)
echo  [OK] Dependencies ready.
echo.
echo  [..] Building RigDeck.exe - this takes a minute...
echo.
python -m PyInstaller --onefile --noconsole ^
    --name RigDeck ^
    --icon rigdeck.ico ^
    --hidden-import truck_telemetry ^
    --hidden-import pydirectinput ^
    rigdeck.py
if errorlevel 1 (
    echo  [X] Build failed. Scroll up to see the error.
    pause
    exit /b 1
)
echo.
echo  ============================================================
echo    DONE.   Your app is here:   dist\RigDeck.exe
echo  ============================================================
echo.
pause
