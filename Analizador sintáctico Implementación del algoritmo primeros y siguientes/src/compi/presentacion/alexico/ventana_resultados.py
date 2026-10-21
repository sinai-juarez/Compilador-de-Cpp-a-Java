"""Subventanas con las salidas del análisis léxico del AFD.

Como en el analizador en Flex, cada salida (tira de tokens, tabla de
símbolos y tabla de errores) se abre en su propia ventana, cada una con
un botón "Guardar como..." que exporta su .txt con el mismo formato que
produce el analizador en Flex.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .estilos import COLORES
from .tabla_errores import TablaErrores
from .tabla_simbolos import TablaSimbolos
from .tira_tokens import TiraTokens, token_mostrado


class VentanaTabla(tk.Toplevel):
    """Ventana con una sola tabla de resultados y su botón para guardarla."""

    def __init__(self, padre, titulo, geometria, tabla_cls, resumen,
                 nombre_sugerido, contenido_txt):
        super().__init__(padre)
        self.title(titulo)
        self.geometry(geometria)
        self.minsize(360, 220)
        self.configure(bg=COLORES["fondo"])
        # Sin transient(): una ventana "transitoria" pierde los botones de
        # minimizar y maximizar en Windows y en varios escritorios de Linux.
        self.resizable(True, True)
        self._nombre_sugerido = nombre_sugerido
        self._contenido_txt = contenido_txt

        # La barra se empaqueta primero (abajo) para que siempre quede
        # visible aunque la ventana sea baja, como la de errores.
        barra = ttk.Frame(self)
        barra.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        self._etiqueta = ttk.Label(barra, text=resumen)
        self._etiqueta.pack(side="left")
        ttk.Button(barra, text="💾  Guardar como...",
                   command=self._guardar_como).pack(side="right")

        self.tabla = tabla_cls(self)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=(10, 4))

    def _guardar_como(self):
        ruta = filedialog.asksaveasfilename(
            parent=self, title="Guardar como",
            initialfile=self._nombre_sugerido, defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"),
                       ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                f.write(self._contenido_txt)
        except OSError as e:
            messagebox.showerror("Error al guardar", str(e), parent=self)
            return
        self._etiqueta.config(text=f"Guardado en {ruta} ✓")


def abrir_ventanas_resultados(padre, tokens, errores):
    """Abre las 3 subventanas (mismas posiciones que las de Flex) y
    devuelve (ventanas, total de símbolos)."""
    simbolos = identificadores(tokens)

    tira = VentanaTabla(
        padre, "Tira de tokens (AFD)", "820x600+80+60", TiraTokens,
        f"♡  {len(tokens)} tokens", "tiraTokens.txt", texto_tira(tokens))
    tira.tabla.mostrar(tokens)

    tabla_simbolos = VentanaTabla(
        padre, "Tabla de símbolos (AFD)", "420x600+920+60", TablaSimbolos,
        f"♡  {len(simbolos)} símbolos", "tablaSimbolos.txt",
        texto_simbolos(simbolos))
    tabla_simbolos.tabla.mostrar(tokens)

    tabla_errores = VentanaTabla(
        padre, "Tabla de errores (AFD)", "820x300+80+680", TablaErrores,
        f"⚠  {len(errores)} errores", "errores.txt", texto_errores(errores))
    tabla_errores.tabla.mostrar(errores)

    return [tira, tabla_simbolos, tabla_errores], len(simbolos)


# ----------------------------------------------------------------------
# Contenido de los .txt (mismo formato que produce el analizador en Flex)
# ----------------------------------------------------------------------

def identificadores(tokens):
    simbolos = []
    for t in tokens:
        if t.token == "IDENTIFICADOR" and t.lexema not in simbolos:
            simbolos.append(t.lexema)
    return simbolos


def texto_tira(tokens):
    lineas = [f"{'No linea':<9}{'lexema':<26} token"]
    lineas += [f"{t.linea:<9}{t.lexema:<26} {token_mostrado(t)}"
               for t in tokens]
    return "\n".join(lineas) + "\n"


def texto_simbolos(simbolos):
    lineas = [f"{'#':<5}Identificador"]
    lineas += [f"{i:<5}{s}" for i, s in enumerate(simbolos, 1)]
    return "\n".join(lineas) + "\n"


def texto_errores(errores):
    lineas = [f"{'#':<5}{'Línea':<8}{'Columna':<10}{'Carácter':<11}Descripción"]
    lineas += [f"{i:<5}{e.linea:<8}{e.columna:<10}{e.caracter:<11}{e.mensaje}"
               for i, e in enumerate(errores, 1)]
    return "\n".join(lineas) + "\n"
