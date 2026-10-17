@echo off
chcp 65001 > nul
cd /d "%~dp0"
powershell -NoProfile -Command "Start-Process python -ArgumentList 'persian_gui_app\main.py' -Verb RunAs -WorkingDirectory '%~dp0'"
