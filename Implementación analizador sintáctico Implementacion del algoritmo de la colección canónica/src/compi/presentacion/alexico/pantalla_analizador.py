"""Base de las pantallas de los analizadores léxicos (AFD y Flex).

Contiene lo que comparten: encabezado, panel "Programa fuente" y editor.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .editor_codigo import EditorCodigo
from .estilos import COLORES
from .iconos import con_icono, crear_titulo


class PantallaAnalizador(tk.Frame):
    """`padre` es la VentanaPrincipal que orquesta las pantallas."""

    def __init__(self, padre, titulo):
        super().__init__(padre.root, bg=COLORES["fondo"])
        self.padre = padre
        self.btn_analizar = None
        self._crear_encabezado(titulo)

    def _crear_encabezado(self, titulo):
        encabezado = tk.Frame(self, bg=COLORES["fondo"])
        encabezado.pack(fill="x", padx=18, pady=(10, 2))
        crear_titulo(encabezado, titulo).pack()
        ttk.Label(encabezado, text="Compilador C++ → Java").pack(pady=(0, 5))

    def _crear_panel_fuente(self, al_analizar=None):
        """Panel 'Programa fuente'; el botón Analizar solo se crea si la
        pantalla lo usa."""
        superior = ttk.LabelFrame(self, text="  Programa fuente  ")
        superior.pack(fill="x", padx=18, pady=(2, 8))

        ttk.Label(superior, text="Selecciona un programa C/C++:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(superior, **con_icono("♡  Abrir archivo"),
                   command=self.abrir_archivo).grid(
            row=0, column=1, padx=7, pady=10)
        self.lbl_archivo = ttk.Label(superior,
                                     text="Ningún archivo seleccionado")
        self.lbl_archivo.grid(row=0, column=2, padx=8, pady=10, sticky="w")

        if al_analizar is not None:
            self.btn_analizar = ttk.Button(superior, **con_icono("✿  Analizar"),
                                           command=al_analizar,
                                           state="disabled")
            self.btn_analizar.grid(row=1, column=1, padx=7, pady=(0, 10),
                                   sticky="w")
        ttk.Button(superior, **con_icono("♡  Limpiar"), command=self.limpiar).grid(
            row=1, column=2, padx=8, pady=(0, 10), sticky="w")

    def _crear_editor(self):
        self.editor = EditorCodigo(self, al_modificar=self._editor_modificado)
        self.editor.pack(fill="both", expand=True, padx=18, pady=(0, 8))

    def _editor_modificado(self):
        if self.btn_analizar is None:
            return
        if self.editor.contenido().strip():
            self.btn_analizar.config(state="normal")
        else:
            self.btn_analizar.config(state="disabled")

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Abrir programa fuente",
            filetypes=[
                ("Archivos C/C++", "*.cpp *.cc *.cxx *.c *.h *.hpp"),
                ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            contenido = self.padre.lector.cargar_archivo(ruta)
            self.editor.cargar(contenido)
            self.lbl_archivo.config(text=ruta)
            if self.btn_analizar is not None:
                self.btn_analizar.config(state="normal")
            self.padre.mostrar_estado("♡  Archivo cargado. Presiona Analizar.")
        except OSError as e:
            messagebox.showerror("Error al abrir archivo", str(e))

    def limpiar(self):
        self.editor.limpiar()
        self.lbl_archivo.config(text="Ningún archivo seleccionado")
        if self.btn_analizar is not None:
            self.btn_analizar.config(state="disabled")
        self.cerrar_resultados()
        self.padre.mostrar_estado("♡  Todo ha sido limpiado.")

    def cerrar_resultados(self):
        """Cierra las ventanas de resultados; cada pantalla la implementa."""
