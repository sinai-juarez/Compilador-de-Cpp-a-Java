#!/bin/sh
# Abre la interfaz del compilador (colección canónica) en Linux y macOS.
cd "$(dirname "$0")/src" || exit 1

for python in python3 python; do
    if command -v "$python" >/dev/null 2>&1 &&
       "$python" -c "import sys, tkinter; sys.exit(sys.version_info < (3, 9))" 2>/dev/null; then
        exec "$python" -m compi.presentacion.compilador
    fi
done

echo "No se encontró Python 3.9 o superior con Tkinter."
echo "  Ubuntu/Debian: sudo apt install python3 python3-tk flex gcc"
echo "  Fedora:        sudo dnf install python3 python3-tkinter flex gcc"
echo "  macOS:         instala Python desde https://www.python.org/downloads/"
echo "                 (o con Homebrew: brew install python-tk flex)"
exit 1
