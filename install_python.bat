@echo off

set "PYTHON_VERSION=3.10.0"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"
set "PYTHON_EXE=python-installer.exe"

curl -L -o %PYTHON_EXE% %PYTHON_URL%

start /wait %PYTHON_EXE% /quiet /passive InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Include_doc=0

del %PYTHON_EXE%
