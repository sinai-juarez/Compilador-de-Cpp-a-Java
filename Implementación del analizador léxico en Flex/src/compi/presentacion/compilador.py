"""Clase Compilador: punto de entrada del programa.

Crea la ventana principal, que orquesta a las demás ventanas.
"""

import os
import sys
import tkinter as tk

if __package__ in (None, ""):
    # Ejecutado como script: agregar src/ al path para importar "compi".
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))

from compi.presentacion.ventana_principal import VentanaPrincipal


class Compilador:

    @staticmethod
    def main():
        root = tk.Tk()
        VentanaPrincipal(root)
        root.mainloop()


if __name__ == "__main__":
    Compilador.main()
