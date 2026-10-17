@echo off
chcp 65001 > nul
title Antigravity Unlocker - Persian GUI
cd /d "%~dp0"
echo Starting Antigravity Unlocker Persian GUI...
python persian_gui_app\main.py
if %errorlevel% neq 0 (
    echo.
    echo An error occurred while launching. Press any key to exit.
    pause > nul
)
