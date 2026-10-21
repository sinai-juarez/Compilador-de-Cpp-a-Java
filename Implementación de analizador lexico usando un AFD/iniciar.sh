#!/bin/sh
# Abre la interfaz del analizador léxico en Linux y macOS.
cd "$(dirname "$0")" || exit 1

for python in python3 python; do
    if command -v "$python" >/dev/null 2>&1 &&
       "$python" -c "import sys, tkinter; sys.exit(sys.version_info < (3, 9))" 2>/dev/null; then
        exec "$python" "src/interfaz.py"
    fi
done

echo "No se encontró Python 3.9 o superior con Tkinter."
echo "  Ubuntu/Debian: sudo apt install python3 python3-tk"
echo "  Fedora:        sudo dnf install python3 python3-tkinter"
echo "  macOS:         instala Python desde https://www.python.org/downloads/"
echo "                 (o con Homebrew: brew install python-tk)"
exit 1
