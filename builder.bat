@echo off
title Candy
color 0d

python --version 2>&1 | findstr " 3.12" >nul
if not %errorlevel% == 0 (
    echo Only Python 3.12.x is supported by Witch. Please install Python 3.12.0.
    pause
    exit
)

git --version 2>&1>nul
if %errorlevel% == 9009 (
    echo git is either not installed or not added to path! You can install it here https://git-scm.com/download/win
    pause
    exit
)


pip uninstall -y pyinstaller
pip install -r requirements.txt
cls

py -3.12 builder/main.py
pause
