"""Presentación de la tabla de símbolos/identificadores."""

import tkinter as tk
from tkinter import ttk

from .tabla_base import crear_tabla


class TablaSimbolos(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        marco, self.tabla = crear_tabla(
            self, ("numero", "identificador"),
            ("#", "Identificador"), (60, 500), solo_vertical=True,
        )
        marco.pack(fill="both", expand=True)

    def mostrar(self, tokens):
        """Lista cada identificador una sola vez y devuelve cuántos hay."""
        self.limpiar()
        simbolos = []
        for token in tokens:
            if token.token == "IDENTIFICADOR" and token.lexema not in simbolos:
                simbolos.append(token.lexema)

        for i, simbolo in enumerate(simbolos, 1):
            self.tabla.insert("", tk.END, values=(i, simbolo))
        return len(simbolos)

    def limpiar(self):
        self.tabla.delete(*self.tabla.get_children())
