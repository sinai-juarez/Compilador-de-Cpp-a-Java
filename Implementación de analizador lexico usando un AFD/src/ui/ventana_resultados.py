"""Subventana que agrupa las salidas del análisis léxico."""

import tkinter as tk
from tkinter import ttk

from .estilos import COLORES
from .tabla_errores import TablaErrores
from .tabla_simbolos import TablaSimbolos
from .tira_tokens import TiraTokens


class VentanaResultados(tk.Toplevel):
    def __init__(self, padre):
        super().__init__(padre)
        self.title("Resultados del análisis léxico")
        self.geometry(f"980x620+{padre.winfo_rootx() + 40}"
                      f"+{padre.winfo_rooty() + 60}")
        self.minsize(700, 420)
        self.configure(bg=COLORES["fondo"])
        self.transient(padre)

        self.resumen = ttk.Label(self, style="Titulo.TLabel")
        self.resumen.pack(fill="x", padx=18, pady=(12, 4))

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
