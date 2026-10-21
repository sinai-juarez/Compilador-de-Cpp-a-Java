@echo off
rem Abre la interfaz del analizador lexico en Windows.
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    py -3 "src\interfaz.py"
    if errorlevel 1 pause
    exit /b
)

where python >nul 2>nul
if not errorlevel 1 (
    python "src\interfaz.py"
    if errorlevel 1 pause
    exit /b
)

echo No se encontro Python 3.9 o superior.
echo Instalalo desde https://www.python.org/downloads/
echo y marca la casilla "Add python.exe to PATH" durante la instalacion.
pause
