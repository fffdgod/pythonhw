@echo off
rem ============================================================
rem  Run this project with the C:\qt310 virtual environment.
rem  Why: PyQt5 must live on an ASCII-only path, otherwise Qt
rem  cannot locate its platform plugin (qwindows.dll) because
rem  the Windows user name "xiaohuang" is non-ASCII.
rem ============================================================

set "VENV_PY=C:\qt310\Scripts\python.exe"

if not exist "%VENV_PY%" (
    echo [ERROR] Virtual environment not found: %VENV_PY%
    echo Create it with:
    echo     python -m venv C:\qt310
    echo     C:\qt310\Scripts\pip install PyQt5
    pause
    exit /b 1
)

cd /d "%~dp0src"
"%VENV_PY%" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] The program exited abnormally. See the message above.
    pause
)
