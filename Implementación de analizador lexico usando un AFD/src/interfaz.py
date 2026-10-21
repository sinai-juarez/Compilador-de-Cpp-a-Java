"""Punto de entrada de la interfaz gráfica del compilador."""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

MODULOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modulos")
if MODULOS_DIR not in sys.path:
    sys.path.insert(0, MODULOS_DIR)

from afd_lexico import AFDAlexico
from analizador_lexico import AnalizadorLexico
from lector_archivo import LectorArchivo
from ui.editor_codigo import EditorCodigo
from ui.estilos import COLORES, FUENTES, configurar_estilos
from ui.ventana_resultados import VentanaResultados


class InterfazAnalizador:

    def __init__(self, root):
        self.root = root
        self.root.title("Compilador C++ → Java | Analizador Léxico")
        self.root.geometry("1180x780")
        self.root.minsize(950, 650)
        self.root.configure(bg=COLORES["fondo"])
        self.lector = LectorArchivo()
        self.analizador = None
        self.ventana_resultados = None
        configurar_estilos(self.root)
        self._crear_menu()
        self._crear_interfaz()

    def _crear_menu(self):
        barra = tk.Menu(self.root, bg=COLORES["rosa_claro"],
                        fg=COLORES["texto"],
                        activebackground=COLORES["rosa"],
                        activeforeground=COLORES["blanco"])

        menu_archivo = tk.Menu(barra, tearoff=0, bg=COLORES["rosa_muy_claro"],
                               fg=COLORES["texto"],
                               activebackground=COLORES["rosa"],
                               activeforeground=COLORES["blanco"])
        menu_archivo.add_command(label="Abrir programa fuente",
                                 command=self.abrir_archivo)
        menu_archivo.add_command(label="Limpiar", command=self.limpiar)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.destroy)

        menu_analizadores = tk.Menu(barra, tearoff=0,
                                    bg=COLORES["rosa_muy_claro"],
                                    fg=COLORES["texto"],
                                    activebackground=COLORES["rosa"],
                                    activeforeground=COLORES["blanco"])
        menu_analizadores.add_command(label="Analizador léxico",
                                      command=lambda: None)
        menu_analizadores.add_command(
            label="Analizador sintáctico",
            command=lambda: messagebox.showinfo(
                "Información", "Módulo sintáctico pendiente."))
        menu_analizadores.add_command(
            label="Analizador semántico",
            command=lambda: messagebox.showinfo(
                "Información", "Módulo semántico pendiente."))

        barra.add_cascade(label="Archivo", menu=menu_archivo)
        barra.add_cascade(label="Analizadores", menu=menu_analizadores)
        self.root.config(menu=barra)

    def _crear_interfaz(self):
        encabezado = tk.Frame(self.root, bg=COLORES["fondo"])
        encabezado.pack(fill="x", padx=18, pady=(10, 2))
        ttk.Label(encabezado, text="✿  ANALIZADOR LÉXICO  ✿",
                  style="Titulo.TLabel").pack()
        ttk.Label(encabezado, text="Compilador C++ → Java").pack(pady=(0, 5))

        superior = ttk.LabelFrame(self.root, text="  Programa fuente  ")
        superior.pack(fill="x", padx=18, pady=(2, 8))

        ttk.Label(superior, text="Selecciona un programa C/C++:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")

        self.btn_abrir = ttk.Button(superior, text="♡  Abrir archivo",
                                    command=self.abrir_archivo)
        self.btn_abrir.grid(row=0, column=1, padx=7, pady=10)

        self.lbl_archivo = ttk.Label(superior,
                                     text="Ningún archivo seleccionado")
        self.lbl_archivo.grid(row=0, column=2, padx=8, pady=10, sticky="w")

        self.btn_analizar = ttk.Button(superior, text="✿  Analizar",
                                       command=self.analizar,
                                       state="disabled")
        self.btn_analizar.grid(row=1, column=1, padx=7, pady=(0, 10),
                               sticky="w")

        ttk.Button(superior, text="♡  Limpiar", command=self.limpiar).grid(
            row=1, column=2, padx=8, pady=(0, 10), sticky="w")

        self.editor = EditorCodigo(self.root,
                                   al_modificar=self._editor_modificado)
        self.editor.pack(fill="both", expand=True, padx=18, pady=(0, 8))

        estado_frame = tk.Frame(self.root, bg=COLORES["rosa_claro"],
                                highlightbackground=COLORES["rosa_borde"],
                                highlightthickness=1)
        estado_frame.pack(fill="x", padx=18, pady=(0, 8))
        self.estado = tk.Label(
            estado_frame,
            text="♡  Listo. Abre un archivo C/C++ o escribe código.",
            bg=COLORES["rosa_claro"], fg=COLORES["texto"],
            font=(FUENTES["ui"], 9), anchor="w", padx=10, pady=5)
        self.estado.pack(fill="x")

    def _editor_modificado(self):
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
            contenido = self.lector.cargar_archivo(ruta)
            self.editor.cargar(contenido)
            self.lbl_archivo.config(text=ruta)
            self.btn_analizar.config(state="normal")
            self.estado.config(text="♡  Archivo cargado. Presiona Analizar.")
        except OSError as e:
            messagebox.showerror("Error al abrir archivo", str(e))

    def analizar(self):
        codigo = self.editor.contenido()
        if not codigo.strip():
            messagebox.showwarning(
                "Analizador léxico", "No hay código fuente para analizar.")
            return

        try:
            afd = AFDAlexico()
            self.analizador = AnalizadorLexico(codigo, afd)
            tokens = self.analizador.analizar()
            errores = self.analizador.errores

            if (self.ventana_resultados is None
                    or not self.ventana_resultados.winfo_exists()):
                self.ventana_resultados = VentanaResultados(self.root)
            total_simbolos = self.ventana_resultados.mostrar(tokens, errores)
            self.estado.config(
                text=(f"♡  Análisis terminado: {len(tokens)} tokens, "
                      f"{total_simbolos} símbolos y "
                      f"{len(errores)} errores."))

        except Exception as e:
            messagebox.showerror(
                "Error durante el análisis", f"{type(e).__name__}: {e}")

    def limpiar(self):
        self.editor.limpiar()
        self.lbl_archivo.config(text="Ningún archivo seleccionado")
        self.btn_analizar.config(state="disabled")
        self.analizador = None
        if (self.ventana_resultados is not None
                and self.ventana_resultados.winfo_exists()):
            self.ventana_resultados.destroy()
        self.ventana_resultados = None
        self.estado.config(text="♡  Todo ha sido limpiado.")


if __name__ == "__main__":
    root = tk.Tk()
    InterfazAnalizador(root)
    root.mainloop()
