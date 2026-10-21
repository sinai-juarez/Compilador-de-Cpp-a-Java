"""Clase VentanaPrincipal: ventana padre del compilador.

Crea la barra de menús y submenús, muestra el logo de la UTM como pantalla
de inicio y cambia a la pantalla del analizador que elija el usuario.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox

from compi import RAIZ_PROYECTO
from compi.persistencia.analizadorLexico.generales.lector_archivo import LectorArchivo
from compi.presentacion.alexico.estilos import COLORES, FUENTES, configurar_estilos
from compi.presentacion.alexico.ventana_alexico import VentanaALexico
from compi.presentacion.alexico.ventana_alexico_flex import VentanaALexicoFlex
from compi.presentacion.asintactico.ventana_primeros_siguientes import (
    VentanaPrimerosSiguientes)

RUTA_LOGO = os.path.join(RAIZ_PROYECTO, "imagenes", "logo_utm.png")

MENSAJES_ESTADO = {
    "inicio": "♡  Elige un analizador en el menú Analizadores.",
    "afd": "♡  Analizador léxico (AFD). Abre un archivo C/C++ o escribe código.",
    "flex": "♡  Analizador léxico (Flex). Abre un archivo C/C++ o escribe código.",
}


class VentanaPrincipal:

    def __init__(self, root):
        self.root = root
        self.root.title("Compilador C++ → Java | Analizador Léxico")
        self.root.geometry("1180x780")
        self.root.minsize(950, 650)
        self.root.configure(bg=COLORES["fondo"])
        self.lector = LectorArchivo()
        self._logo = None
        configurar_estilos(self.root)
        self.ini()

    def ini(self):
        self.menu_bar = tk.Menu(self.root, bg=COLORES["rosa_claro"],
                                fg=COLORES["texto"],
                                activebackground=COLORES["rosa"],
                                activeforeground=COLORES["blanco"])
        self.menu_archivo()
        self.menu_analizadores()
        self.root.config(menu=self.menu_bar)

        self._crear_barra_estado()
        self.pantallas = {
            "inicio": self._crear_pantalla_inicio(),
            "afd": VentanaALexico(self),
            "flex": VentanaALexicoFlex(self),
        }
        self.pantalla_actual = None
        self.mostrar_pantalla("inicio")

    # ------------------------------------------------------------------
    # MENÚS
    # ------------------------------------------------------------------

    def _crear_menu(self, padre):
        return tk.Menu(padre, tearoff=0, bg=COLORES["rosa_muy_claro"],
                       fg=COLORES["texto"],
                       activebackground=COLORES["rosa"],
                       activeforeground=COLORES["blanco"])

    def menu_archivo(self):
        mn_archivo = self._crear_menu(self.menu_bar)
        mn_archivo.add_command(label="Abrir programa fuente",
                               command=self.abrir_archivo)
        mn_archivo.add_command(label="Limpiar", command=self.limpiar)
        mn_archivo.add_separator()
        mn_archivo.add_command(label="Inicio",
                               command=lambda: self.mostrar_pantalla("inicio"))
        mn_archivo.add_command(label="Salir", command=self.root.destroy)
        self.menu_bar.add_cascade(label="Archivo", menu=mn_archivo)

    def menu_analizadores(self):
        mn_analizadores = self._crear_menu(self.menu_bar)

        # Submenú que se despliega al pasar el mouse sobre "Analizador léxico".
        mn_alexico = self._crear_menu(mn_analizadores)
        mn_alexico.add_command(label="Analizador léxico_Flex",
                               command=lambda: self.mostrar_pantalla("flex"))
        mn_alexico.add_command(label="Analizador léxico_AFD",
                               command=lambda: self.mostrar_pantalla("afd"))

        mn_analizadores.add_cascade(label="Analizador léxico", menu=mn_alexico)
        self.menu_analizador_sintactico(mn_analizadores)
        mn_analizadores.add_command(
            label="Analizador semántico",
            command=lambda: messagebox.showinfo(
                "Información", "Módulo semántico pendiente."))
        self.menu_bar.add_cascade(label="Analizadores", menu=mn_analizadores)

    def menu_analizador_sintactico(self, mn_analizadores):
        """Submenú "Analizador sintáctico": cada opción abre la ventana
        hija de su algoritmo."""
        mn_asintactico = self._crear_menu(mn_analizadores)
        mn_asintactico.add_command(label="Algoritmo Primeros y Siguientes",
                                   command=self.primeros_siguientes)
        mn_analizadores.add_cascade(label="Analizador sintáctico",
                                    menu=mn_asintactico)

    def primeros_siguientes(self):
        """Abre la ventana del algoritmo de Primeros y Siguientes como
        ventana hija modal (como VentanaAThompson(this, true) en el PDF)."""
        VentanaPrimerosSiguientes(self, True)

    # ------------------------------------------------------------------
    # PANTALLAS
    # ------------------------------------------------------------------

    def _crear_barra_estado(self):
        # Se empaqueta primero para que siempre quede visible abajo, sin
        # importar qué pantalla esté activa.
        estado_frame = tk.Frame(self.root, bg=COLORES["rosa_claro"],
                                highlightbackground=COLORES["rosa_borde"],
                                highlightthickness=1)
        estado_frame.pack(side="bottom", fill="x", padx=18, pady=(0, 8))
        self.estado = tk.Label(
            estado_frame, text=MENSAJES_ESTADO["inicio"],
            bg=COLORES["rosa_claro"], fg=COLORES["texto"],
            font=(FUENTES["ui"], 9), anchor="w", padx=10, pady=5)
        self.estado.pack(fill="x")

    def _crear_pantalla_inicio(self):
        pantalla = tk.Frame(self.root, bg=COLORES["fondo"])
        try:
            logo = tk.PhotoImage(file=RUTA_LOGO)
            # Reducir el logo para que quepa holgadamente en la ventana.
            factor = max(1, -(-logo.height() // 560))
            self._logo = logo.subsample(factor, factor)
            tk.Label(pantalla, image=self._logo,
                     bg=COLORES["fondo"]).pack(expand=True)
        except tk.TclError:
            ttk.Label(pantalla, text="Universidad Tecnológica de la Mixteca",
                      style="Titulo.TLabel").pack(expand=True)
        return pantalla

    def mostrar_pantalla(self, nombre):
        if self.pantalla_actual is not None:
            self.pantallas[self.pantalla_actual].pack_forget()
        self.pantallas[nombre].pack(fill="both", expand=True)
        self.pantalla_actual = nombre
        self.mostrar_estado(MENSAJES_ESTADO[nombre])

    def mostrar_estado(self, texto):
        self.estado.config(text=texto)

    # ------------------------------------------------------------------
    # ACCIONES DEL MENÚ ARCHIVO
    # ------------------------------------------------------------------

    def abrir_archivo(self):
        if self.pantalla_actual == "inicio":
            messagebox.showinfo(
                "Abrir programa fuente",
                "Primero elige un analizador en el menú Analizadores.")
            return
        self.pantallas[self.pantalla_actual].abrir_archivo()

    def limpiar(self):
        """Limpia la pantalla activa; desde el inicio limpia ambas."""
        if self.pantalla_actual == "inicio":
            self.pantallas["afd"].limpiar()
            self.pantallas["flex"].limpiar()
        else:
            self.pantallas[self.pantalla_actual].limpiar()
