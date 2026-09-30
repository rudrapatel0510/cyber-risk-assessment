@echo off
cd /d "%~dp0"

echo Starting the Risk Assessment window...
echo.

if exist "C:\Python313\python.exe" (
    "C:\Python313\python.exe" app.py
) else (
    py app.py
)

if errorlevel 1 (
    echo.
    echo The app did not start. Make sure Python is installed.
    pause
)
