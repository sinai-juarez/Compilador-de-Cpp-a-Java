"""Clase VentanaPrimerosSiguientes: ventana "Cálculo de primeros y siguientes".

Como la VentanaAThompson del ejemplo de arquitectura (un JDialog), es una
ventana hija de la VentanaPrincipal (tk.Toplevel); el constructor recibe la
ventana padre y si será modal (mientras esté abierta, la ventana principal
no se puede usar).

Interfaz de la Asignación 3: botón Abrir para seleccionar el archivo de la
gramática, la ruta seleccionada, botones Analizar y Limpiar, la gramática a
la izquierda y los conjuntos PRIMEROS y SIGUIENTES a la derecha.
"""

import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from compi import RAIZ_PROYECTO
from compi.persistencia.analizadorSintacticoLR.generales.gramatica import (
    ErrorGramatica, LectorGramatica)
from compi.persistencia.analizadorSintacticoLR.primerosYsiguientes.primeros_siguientes import (
    PrimerosSiguientes)
from compi.presentacion.alexico.estilos import COLORES, FUENTES
from compi.presentacion.alexico.iconos import con_icono, crear_titulo

def carpeta_recursos(nombre):
    """Carpeta de recursos del proyecto (gramaticas, gramaticasAumentadas…).

    En el .exe, sys._MEIPASS es temporal: los archivos de ejemplo se copian
    a una carpeta con el mismo nombre junto al .exe (sin sobrescribir los
    del usuario)."""
    if not getattr(sys, "frozen", False):
        return os.path.join(RAIZ_PROYECTO, nombre)
    carpeta = os.path.join(os.path.dirname(sys.executable), nombre)
    try:
        shutil.copytree(os.path.join(sys._MEIPASS, nombre), carpeta,
                        dirs_exist_ok=True,
                        copy_function=lambda o, d: os.path.exists(d)
                        or shutil.copyfile(o, d))
    except OSError:
        carpeta = os.path.join(sys._MEIPASS, nombre)
    return carpeta


CARPETA_GRAMATICAS = carpeta_recursos("gramaticas")

AYUDA_FORMATO = (
    "Formato: línea 1 = no terminales, línea 2 = terminales, línea 3 "
    "(opcional) = símbolo inicial; después una regla por línea: A → α. "
    "Usa ε (o eps) para la cadena vacía. Si | no es terminal, se permiten "
    "alternativas A → α | β.")


class VentanaPrimerosSiguientes(tk.Toplevel):
    """`padre` es la VentanaPrincipal que orquesta las ventanas."""

    def __init__(self, padre, modal):
        super().__init__(padre.root)
        self.padre = padre
        self.lector = LectorGramatica()
        self.resultado = None
        self.ini()
        if modal:
            self.grab_set()

    def ini(self):
        self.title("Cálculo de primeros y siguientes")
        self.geometry("1050x680")
        self.minsize(800, 520)
        self.configure(bg=COLORES["fondo"])
        self._crear_encabezado()
        self._crear_formulario()
        self._crear_paneles()
        self._crear_barra_estado()

    # ------------------------------------------------------------------
    # COMPONENTES
    # ------------------------------------------------------------------

    def _crear_encabezado(self):
        encabezado = tk.Frame(self, bg=COLORES["fondo"])
        encabezado.pack(fill="x", padx=18, pady=(10, 2))
        crear_titulo(encabezado, "✿  CÁLCULO DE PRIMEROS Y SIGUIENTES  ✿").pack()
        ttk.Label(encabezado, text="Analizador sintáctico · Compilador "
                  "C++ → Java").pack(pady=(0, 5))

    def _crear_formulario(self):
        formulario = ttk.LabelFrame(self, text="  Gramática  ")
        formulario.pack(fill="x", padx=18, pady=(2, 8))
        formulario.columnconfigure(2, weight=1)

        ttk.Label(formulario, text="Selecciona una gramática:").grid(
            row=0, column=0, padx=10, pady=(10, 4), sticky="w")
        ttk.Button(formulario, **con_icono("♡  Abrir"),
                   command=self.abrir_archivo).grid(
            row=0, column=1, padx=7, pady=(10, 4), sticky="w")

        ttk.Label(formulario, text="Gramática seleccionada:").grid(
            row=1, column=0, padx=10, pady=4, sticky="w")
        self.lbl_archivo = ttk.Label(formulario,
                                     text="Ninguna gramática seleccionada")
        self.lbl_archivo.grid(row=1, column=1, columnspan=2, padx=7, pady=4,
                              sticky="w")

        botones = ttk.Frame(formulario)
        botones.grid(row=2, column=0, columnspan=3, padx=10, pady=(4, 10),
                     sticky="w")
        self.btn_analizar = ttk.Button(botones, **con_icono("✿  Analizar"),
                                       command=self.analizar,
                                       state="disabled")
        self.btn_analizar.pack(side="left")
        ttk.Button(botones, **con_icono("♡  Limpiar"),
                   command=self.limpiar).pack(side="left", padx=7)
        self.btn_guardar = ttk.Button(botones, **con_icono("💾  Guardar resultados"),
                                      command=self.guardar_resultados,
                                      state="disabled")
        self.btn_guardar.pack(side="left")

    def _crear_paneles(self):
        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill="both", expand=True, padx=18, pady=(0, 8))
        cuerpo.columnconfigure(0, weight=1, uniform="paneles")
        cuerpo.columnconfigure(1, weight=1, uniform="paneles")
        cuerpo.rowconfigure(0, weight=1)

        izq = ttk.LabelFrame(cuerpo, text="  Gramática (editable)  ")
        izq.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self.txt_gramatica = self._crear_texto(izq, editable=True,
                                               ajustar=False)
        self.txt_gramatica.bind("<<Modified>>", self._gramatica_modificada)
        ttk.Label(izq, text=AYUDA_FORMATO, wraplength=440,
                  font=(FUENTES["ui"], 8)).pack(fill="x", padx=8,
                                                pady=(0, 6))

        der = ttk.LabelFrame(cuerpo, text="  Primeros y siguientes  ")
        der.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        self.txt_resultados = self._crear_texto(der, editable=False,
                                                ajustar=True)
        self.txt_resultados.tag_configure(
            "titulo", foreground=COLORES["rosa_oscuro"],
            font=(FUENTES["codigo"], 11, "bold"))
        self.txt_resultados.tag_configure(
            "info", foreground="#8C6A7A", font=(FUENTES["codigo"], 9))

    def _crear_texto(self, padre, editable, ajustar):
        marco = ttk.Frame(padre)
        marco.pack(fill="both", expand=True, padx=8, pady=8)
        texto = tk.Text(
            marco, wrap="word" if ajustar else "none", undo=editable,
            height=12, font=(FUENTES["codigo"], 11),
            bg=COLORES["blanco"], fg=COLORES["texto"],
            insertbackground=COLORES["rosa_oscuro"],
            selectbackground=COLORES["rosa_claro"],
            selectforeground=COLORES["texto"],
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=COLORES["rosa_borde"], padx=10, pady=8)
        scroll_y = ttk.Scrollbar(marco, orient="vertical",
                                 command=texto.yview)
        scroll_x = ttk.Scrollbar(marco, orient="horizontal",
                                 command=texto.xview)
        texto.configure(yscrollcommand=scroll_y.set,
                        xscrollcommand=scroll_x.set)
        texto.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        if not editable:
            texto.configure(state="disabled")
        return texto

    def _crear_barra_estado(self):
        self.estado = tk.Label(
            self, **con_icono("♡  Abre una gramática o escríbela a la "
                              "izquierda."),
            bg=COLORES["rosa_claro"], fg=COLORES["texto"],
            font=(FUENTES["ui"], 9), anchor="w", padx=10, pady=5)
        self.estado.pack(side="bottom", fill="x", padx=18, pady=(0, 8))

    def mostrar_estado(self, texto):
        self.estado.config(**con_icono(texto))

    # ------------------------------------------------------------------
    # ACCIONES
    # ------------------------------------------------------------------

    def _gramatica_modificada(self, _evento=None):
        self.txt_gramatica.edit_modified(False)
        hay_texto = self.txt_gramatica.get("1.0", "end-1c").strip()
        self.btn_analizar.config(state="normal" if hay_texto else "disabled")

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            parent=self, title="Selecciona una gramática",
            initialdir=CARPETA_GRAMATICAS,
            filetypes=[("Gramáticas", "*.txt"),
                       ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            contenido = self.lector.cargar_archivo(ruta)
        except OSError as e:
            messagebox.showerror("Error al abrir la gramática", str(e),
                                 parent=self)
            return
        self.txt_gramatica.delete("1.0", "end")
        self.txt_gramatica.insert("1.0", contenido)
        self.txt_gramatica.edit_reset()
        self.lbl_archivo.config(text=ruta)
        self._escribir_resultados([])
        self.mostrar_estado("♡  Gramática cargada. Presiona Analizar.")

    def analizar(self):
        texto = self.txt_gramatica.get("1.0", "end-1c")
        try:
            gramatica = self.lector.leer(texto)
        except ErrorGramatica as e:
            self._escribir_resultados([])
            messagebox.showerror("Error en la gramática", str(e),
                                 parent=self)
            self.mostrar_estado("✗  La gramática tiene errores de formato.")
            return

        self.resultado = PrimerosSiguientes(gramatica).calcular()
        self._escribir_resultados([
            (f"Símbolo inicial: {gramatica.inicial}\n", "info"),
            ("No terminales:   " + " ".join(gramatica.no_terminales) + "\n",
             "info"),
            ("Terminales:      " + " ".join(gramatica.terminales) + "\n\n",
             "info"),
            ("PRIMEROS\n", "titulo"),
            ("\n".join(self.resultado.lineas_primeros()) + "\n\n", None),
            ("SIGUIENTES\n", "titulo"),
            ("\n".join(self.resultado.lineas_siguientes()) + "\n", None),
        ])
        self.btn_guardar.config(state="normal")
        self.mostrar_estado(
            f"✓  Primeros y siguientes calculados para "
            f"{len(gramatica.no_terminales)} no terminales y "
            f"{len(gramatica.producciones)} producciones.")

    def guardar_resultados(self):
        if self.resultado is None:
            return
        ruta = filedialog.asksaveasfilename(
            parent=self, title="Guardar resultados",
            initialfile="primeros_siguientes.txt",
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"),
                       ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                f.write(self.resultado.reporte() + "\n")
            self.mostrar_estado(f"💾  Resultados guardados en {ruta}")
        except OSError as e:
            messagebox.showerror("Error al guardar", str(e), parent=self)

    def limpiar(self):
        self.txt_gramatica.delete("1.0", "end")
        self.txt_gramatica.edit_reset()
        self.lbl_archivo.config(text="Ninguna gramática seleccionada")
        self._escribir_resultados([])
        self.mostrar_estado("♡  Todo ha sido limpiado.")

    def _escribir_resultados(self, partes):
        if not partes:
            self.resultado = None
            self.btn_guardar.config(state="disabled")
        self.txt_resultados.configure(state="normal")
        self.txt_resultados.delete("1.0", "end")
        for texto, etiqueta in partes:
            self.txt_resultados.insert("end", texto, etiqueta or ())
        self.txt_resultados.configure(state="disabled")
