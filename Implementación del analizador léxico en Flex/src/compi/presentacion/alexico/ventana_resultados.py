"""Subventana que agrupa las salidas del análisis léxico."""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .estilos import COLORES
from .tabla_errores import TablaErrores
from .tabla_simbolos import TablaSimbolos
from .tira_tokens import TiraTokens, token_mostrado


class VentanaResultados(tk.Toplevel):
    def __init__(self, padre):
        super().__init__(padre)
        self.title("Resultados del análisis léxico")
        self.geometry(f"980x620+{padre.winfo_rootx() + 40}"
                      f"+{padre.winfo_rooty() + 60}")
        self.minsize(700, 420)
        self.configure(bg=COLORES["fondo"])
        # Sin transient(): una ventana "transitoria" pierde los botones de
        # minimizar y maximizar en Windows y en varios escritorios de Linux.
        self.resizable(True, True)

        self._tokens = []
        self._errores = []

        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", padx=18, pady=(12, 4))
        self.resumen = ttk.Label(encabezado, style="Titulo.TLabel")
        self.resumen.pack(side="left")
        ttk.Button(encabezado, text="💾  Exportar resultados (.txt)...",
                  command=self.exportar).pack(side="right")

        self.pestañas = ttk.Notebook(self)
        self.pestañas.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.tira_tokens = TiraTokens(self.pestañas)
        self.tabla_simbolos = TablaSimbolos(self.pestañas)
        self.tabla_errores = TablaErrores(self.pestañas)
        self.pestañas.add(self.tira_tokens, text="  ✿ Tira de tokens  ")
        self.pestañas.add(self.tabla_simbolos, text="  ♡ Tabla de símbolos  ")
        self.pestañas.add(self.tabla_errores, text="  ⚠ Tabla de errores  ")

    def mostrar(self, tokens, errores):
        """Llena las tres tablas, trae la ventana al frente y devuelve el total de símbolos."""
        self._tokens = tokens
        self._errores = errores
        self.tira_tokens.mostrar(tokens)
        total_simbolos = self.tabla_simbolos.mostrar(tokens)
        self.tabla_errores.mostrar(errores)
        self.resumen.config(
            text=(f"♡  {len(tokens)} tokens · {total_simbolos} símbolos · "
                  f"{len(errores)} errores"))
        self.pestañas.select(0)
        self.deiconify()
        self.lift()
        return total_simbolos

    # ------------------------------------------------------------------
    # EXPORTAR: guarda tiraTokens.txt, tablaSimbolos.txt y errores.txt
    # (mismo formato que produce el analizador en Flex) donde el usuario
    # elija.
    # ------------------------------------------------------------------

    def exportar(self):
        carpeta = filedialog.askdirectory(
            parent=self, title="Elige la carpeta donde guardar los .txt")
        if not carpeta:
            return

        ruta_tokens = os.path.join(carpeta, "tiraTokens.txt")
        ruta_simbolos = os.path.join(carpeta, "tablaSimbolos.txt")
        ruta_errores = os.path.join(carpeta, "errores.txt")

        try:
            with open(ruta_tokens, "w", encoding="utf-8", newline="\n") as f:
                f.write(f"{'No linea':<9}{'lexema':<26} token\n")
                for t in self._tokens:
                    f.write(f"{t.linea:<9}{t.lexema:<26} {token_mostrado(t)}\n")

            simbolos = []
            for t in self._tokens:
                if t.token == "IDENTIFICADOR" and t.lexema not in simbolos:
                    simbolos.append(t.lexema)
            with open(ruta_simbolos, "w", encoding="utf-8", newline="\n") as f:
                f.write(f"{'#':<5}Identificador\n")
                for i, s in enumerate(simbolos, 1):
                    f.write(f"{i:<5}{s}\n")

            with open(ruta_errores, "w", encoding="utf-8", newline="\n") as f:
                f.write(f"{'#':<5}{'Línea':<8}{'Columna':<10}{'Carácter':<11}Descripción\n")
                for i, e in enumerate(self._errores, 1):
                    f.write(f"{i:<5}{e.linea:<8}{e.columna:<10}{e.caracter:<11}{e.mensaje}\n")

        except OSError as e:
            messagebox.showerror("Error al exportar", str(e), parent=self)
            return

        messagebox.showinfo(
            "Exportado",
            "Se guardaron:\n\n"
            f"{ruta_tokens}\n{ruta_simbolos}\n{ruta_errores}",
            parent=self)
