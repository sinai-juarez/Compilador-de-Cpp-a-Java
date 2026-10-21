"""Clase Compilador: punto de entrada del programa.

Crea la ventana principal, que orquesta a las demás ventanas.
"""

import os
import subprocess
import sys
import tkinter as tk

if __package__ in (None, ""):
    # Ejecutado como script: agregar src/ al path para importar "compi".
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))

from compi.presentacion.ventana_principal import VentanaPrincipal

# Pythons del sistema con un Tk que sí usa Xft (fuentes suavizadas).
PYTHONS_SISTEMA = ("/usr/bin/python3", "/usr/local/bin/python3")
_VAR_RELANZADO = "COMPI_RELANZADO"
_PRUEBA_XFT = ("import tkinter as tk; r = tk.Tk(); "
               "print(r.tk.call('::tk::pkgconfig', 'get', 'fontsystem')); "
               "r.destroy()")


def _sistema_de_fuentes(root):
    try:
        return root.tk.call("::tk::pkgconfig", "get", "fontsystem")
    except tk.TclError:
        return ""


def _relanzar_con_xft():
    """En Linux, si este Python trae un Tk sin Xft (como el de uv), la
    interfaz solo puede usar fuentes de X11: se ve pixeleada y sin
    emojis. Entonces el programa se vuelve a abrir con el Python del
    sistema, si su Tk sí usa Xft."""
    if not sys.platform.startswith("linux") or os.environ.get(_VAR_RELANZADO):
        return
    root = tk.Tk()
    fuentes = _sistema_de_fuentes(root)
    root.destroy()
    if fuentes == "xft":
        return
    src = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    for python in PYTHONS_SISTEMA:
        if not os.path.exists(python) or os.path.realpath(python) == \
                os.path.realpath(sys.executable):
            continue
        try:
            prueba = subprocess.run([python, "-c", _PRUEBA_XFT],
                                    capture_output=True, text=True,
                                    timeout=10)
        except (OSError, subprocess.SubprocessError):
            continue
        if prueba.stdout.strip() == "xft":
            entorno = dict(os.environ, **{_VAR_RELANZADO: "1"})
            entorno["PYTHONPATH"] = os.pathsep.join(
                filter(None, [src, entorno.get("PYTHONPATH")]))
            os.execve(python, [python, "-m", "compi.presentacion.compilador"],
                      entorno)


class Compilador:

    @staticmethod
    def main():
        _relanzar_con_xft()
        root = tk.Tk()
        VentanaPrincipal(root)
        root.mainloop()


if __name__ == "__main__":
    Compilador.main()
