"""Presentación de errores léxicos."""

import tkinter as tk
from tkinter import ttk

from .tabla_base import crear_tabla


class TablaErrores(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        marco, self.tabla = crear_tabla(
            self, ("numero", "linea", "columna", "caracter", "mensaje"),
            ("#", "Línea", "Columna", "Carácter", "Descripción"), (55, 70, 80, 120, 600),
        )
        marco.pack(fill="both", expand=True)

    def mostrar(self, errores):
        self.limpiar()
        for i, error in enumerate(errores, 1):
            self.tabla.insert(
                "", tk.END,
                values=(i, error.linea, error.columna, error.caracter, error.mensaje),
            )

    def limpiar(self):
        self.tabla.delete(*self.tabla.get_children())
