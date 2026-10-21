"""Compilador C++ → Java organizado por capas (persistencia y presentación)."""

import os
import sys

# Carpeta raíz del proyecto (la que contiene src/, flex/, imagenes/…).
# En el ejecutable de PyInstaller los recursos viven en sys._MEIPASS.
if getattr(sys, "frozen", False):
    RAIZ_PROYECTO = sys._MEIPASS
else:
    RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
