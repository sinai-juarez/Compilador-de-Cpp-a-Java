"""Clase VentanaColeccionCanonica: ventana "Cálculo de la colección canónica".

Como VentanaPrimerosSiguientes, es una ventana hija de la VentanaPrincipal
(tk.Toplevel) y puede ser modal.

Interfaz de la Asignación 4: botón Abrir para seleccionar la gramática, la
ruta seleccionada, botones Analizar y Limpiar; a la izquierda la gramática
de entrada y la gramática aumentada, y a la derecha la colección canónica
(los estados del AFD con sus conjuntos de elementos).
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from compi.persistencia.analizadorSintacticoLR.ccanonica.coleccion_canonica import (
    ColeccionCanonica)
from compi.persistencia.analizadorSintacticoLR.generales.gramatica import (
    ErrorGramatica, LectorGramatica)
from compi.presentacion.alexico.estilos import COLORES, FUENTES
from compi.presentacion.alexico.iconos import con_icono, crear_titulo
from compi.presentacion.asintactico.ventana_primeros_siguientes import (
    carpeta_recursos)

CARPETA_GRAMATICAS_AUMENTADAS = carpeta_recursos("gramaticasAumentadas")

AYUDA_FORMATO = (
    "Formato: línea 1 = no terminales, línea 2 = terminales, línea 3 "
    "(opcional) = símbolo inicial; después una regla por línea: A → α. "
    "La primera regla puede ser la aumentada (E'→E$); si no está, se "
    "agrega S' → S $ automáticamente. Usa ε (o eps) para la cadena vacía.")


class VentanaColeccionCanonica(tk.Toplevel):
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
        self.title("Cálculo de la colección canónica")
        self.geometry("1280x760")
        self.minsize(900, 560)
        self.configure(bg=COLORES["fondo"])
        self._crear_encabezado()
        self._crear_formulario()
        self._crear_barra_estado()
        self._crear_paneles()

    # ------------------------------------------------------------------
    # COMPONENTES
    # ------------------------------------------------------------------

    def _crear_encabezado(self):
        encabezado = tk.Frame(self, bg=COLORES["fondo"])
        encabezado.pack(fill="x", padx=18, pady=(10, 2))
        crear_titulo(encabezado, "✿  CÁLCULO DE LA COLECCIÓN CANÓNICA  ✿").pack()
        ttk.Label(encabezado, text="Analizador sintáctico · Compilador "
                  "C++ → Java").pack(pady=(0, 5))

    def _crear_formulario(self):
        formulario = ttk.LabelFrame(self, text="  Gramática aumentada  ")
        formulario.pack(fill="x", padx=18, pady=(2, 8))
        formulario.columnconfigure(2, weight=1)

        ttk.Label(formulario, text="Seleccione una gramática aumentada:").grid(
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
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.columnconfigure(1, weight=2)
        cuerpo.rowconfigure(0, weight=3)
        cuerpo.rowconfigure(1, weight=2)

        entrada = ttk.LabelFrame(cuerpo, text="  Gramática de entrada "
                                 "(editable)  ")
        entrada.grid(row=0, column=0, sticky="nsew", padx=(0, 6),
                     pady=(0, 6))
        self.txt_gramatica = self._crear_texto(entrada, editable=True)
        self.txt_gramatica.bind("<<Modified>>", self._gramatica_modificada)
        ttk.Label(entrada, text=AYUDA_FORMATO, wraplength=330,
                  font=(FUENTES["ui"], 8)).pack(fill="x", padx=8,
                                                pady=(0, 6))

        aumentada = ttk.LabelFrame(cuerpo, text="  Gramática aumentada  ")
        aumentada.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
        self.txt_aumentada = self._crear_texto(aumentada, editable=False)

        coleccion = ttk.LabelFrame(cuerpo, text="  Colección canónica  ")
        coleccion.grid(row=0, column=1, rowspan=2, sticky="nsew",
                       padx=(6, 0))
        self.txt_coleccion = self._crear_texto(coleccion, editable=False)
        self.txt_coleccion.tag_configure(
            "cerradura", foreground=COLORES["rosa_oscuro"],
            font=(FUENTES["codigo"], 11, "bold"))
        self.txt_coleccion.tag_configure(
            "estado", foreground=COLORES["rosa_oscuro"])
        self.txt_coleccion.tag_configure("existente", foreground="#8C6A7A")
        self.txt_coleccion.tag_configure(
            "aceptacion", foreground="#3E8E5E",
            font=(FUENTES["codigo"], 11, "bold"))

    def _crear_texto(self, padre, editable):
        marco = ttk.Frame(padre)
        marco.pack(fill="both", expand=True, padx=8, pady=8)
        texto = tk.Text(
            marco, wrap="none", undo=editable, height=6,
            font=(FUENTES["codigo"], 11),
            bg=COLORES["blanco"], fg=COLORES["texto"],
            insertbackground=COLORES["rosa_oscuro"],
            selectbackground=COLORES["rosa_claro"],
            selectforeground=COLORES["texto"],
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=COLORES["rosa_borde"], padx=10, pady=8)
        self._con_scroll(marco, texto)
        if not editable:
            texto.configure(state="disabled")
        return texto

    def _con_scroll(self, marco, widget):
        scroll_y = ttk.Scrollbar(marco, orient="vertical",
                                 command=widget.yview)
        scroll_x = ttk.Scrollbar(marco, orient="horizontal",
                                 command=widget.xview)
        widget.configure(yscrollcommand=scroll_y.set,
                         xscrollcommand=scroll_x.set)
        widget.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

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
            parent=self, title="Seleccione una gramática aumentada",
            initialdir=CARPETA_GRAMATICAS_AUMENTADAS,
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
        self._mostrar_resultado(None)
        self.mostrar_estado("♡  Gramática cargada. Presiona Analizar.")

    def analizar(self):
        texto = self.txt_gramatica.get("1.0", "end-1c")
        try:
            gramatica = self.lector.leer(texto)
        except ErrorGramatica as e:
            self._mostrar_resultado(None)
            messagebox.showerror("Error en la gramática", str(e),
                                 parent=self)
            self.mostrar_estado("✗  La gramática tiene errores de formato.")
            return

        self._mostrar_resultado(ColeccionCanonica(gramatica).calcular())
        n = len(self.resultado.estados)
        self.mostrar_estado(f"✓  Colección canónica calculada: {n} estados "
                            f"del AFD (I0 a I{n - 1}).")

    def guardar_resultados(self):
        if self.resultado is None:
            return
        ruta = filedialog.asksaveasfilename(
            parent=self, title="Guardar resultados",
            initialfile="coleccion_canonica.txt",
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"),
                       ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                f.write("GRAMÁTICA AUMENTADA\n")
                f.write("\n".join(self.resultado.lineas_gramatica()))
                f.write("\n\nCOLECCIÓN CANÓNICA\n")
                f.write(self.resultado.reporte() + "\n")
            self.mostrar_estado(f"💾  Resultados guardados en {ruta}")
        except OSError as e:
            messagebox.showerror("Error al guardar", str(e), parent=self)

    def limpiar(self):
        self.txt_gramatica.delete("1.0", "end")
        self.txt_gramatica.edit_reset()
        self.lbl_archivo.config(text="Ninguna gramática seleccionada")
        self._mostrar_resultado(None)
        self.mostrar_estado("♡  Todo ha sido limpiado.")

    # ------------------------------------------------------------------
    # SALIDAS
    # ------------------------------------------------------------------

    def _mostrar_resultado(self, resultado):
        self.resultado = resultado
        self.btn_guardar.config(state="normal" if resultado else "disabled")
        if resultado is None:
            self._escribir(self.txt_aumentada, [])
            self._escribir(self.txt_coleccion, [])
            return
        self._escribir(self.txt_aumentada,
                       [[(linea, None)] for linea in resultado.lineas_gramatica()])
        self._escribir(self.txt_coleccion, resultado.lineas())

    def _escribir(self, texto, lineas):
        """Cada línea es una lista de segmentos (texto, etiqueta)."""
        texto.configure(state="normal")
        texto.delete("1.0", "end")
        for linea in lineas:
            for segmento, etiqueta in linea:
                texto.insert("end", segmento, etiqueta or ())
            texto.insert("end", "\n")
        texto.configure(state="disabled")
