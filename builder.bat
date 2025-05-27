@echo off
title Witch
color 0d

python --version 2>&1 | findstr " 3.11" >nul
if %errorlevel% == 0 (
    echo python 3.11.x and up are not supported by Witch. Please downgrade to python 3.10.0.
    pause
    exit
)

git --version 2>&1>nul
if %errorlevel% == 9009 (
    echo git is either not installed or not added to path! You can install it here https://git-scm.com/download/win
    pause
    exit
)

pip install -r requirements.txt
cls

py -3.10 builder/main.py
pause
