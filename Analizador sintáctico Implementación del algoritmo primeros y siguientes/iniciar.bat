@echo off
rem Abre la interfaz del compilador (primeros y siguientes) en Windows.
cd /d "%~dp0src"

where py >nul 2>nul
if not errorlevel 1 (
    py -3 -m compi.presentacion.compilador
    if errorlevel 1 pause
    exit /b
)

where python >nul 2>nul
if not errorlevel 1 (
    python -m compi.presentacion.compilador
    if errorlevel 1 pause
    exit /b
)

echo No se encontro Python 3.9 o superior.
echo Instalalo desde https://www.python.org/downloads/
echo y marca la casilla "Add python.exe to PATH" durante la instalacion.
pause
