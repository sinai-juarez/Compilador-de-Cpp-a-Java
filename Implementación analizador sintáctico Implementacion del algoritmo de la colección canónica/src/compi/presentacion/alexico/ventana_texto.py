"""Ventana simple de texto: para ver/editar el .l de Flex y para mostrar,
en su propia ventana, cada salida del analizador (tira de tokens, tabla
de símbolos, tabla de errores), tal como pide la Asignación 2.

Siempre trae un botón "Guardar como..." para exportar su contenido a un
.txt donde el usuario elija; si el contenido ya vive en un archivo real
en disco (el que escribe el ejecutable de Flex), también se muestra esa
ruta con un botón para abrir la carpeta que lo contiene.
"""

import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .estilos import COLORES, FUENTES
from .iconos import con_icono


class VentanaTexto(tk.Toplevel):
    def __init__(self, padre, titulo, contenido="", editable=False,
                 al_guardar=None, geometria="800x600",
                 nombre_sugerido="resultado.txt", ruta_origen=None):
        """
        ruta_origen: si el contenido ya está guardado en disco (ej. lo
        escribió el ejecutable de Flex), la ruta a ese archivo. Se
        muestra junto con un botón para abrir esa carpeta.
        """
        super().__init__(padre)
        self.title(titulo)
        self.geometry(geometria)
        self.minsize(360, 220)
        self.configure(bg=COLORES["fondo"])
        # Sin transient(): una ventana "transitoria" pierde los botones de
        # minimizar y maximizar en Windows y en varios escritorios de Linux.
        self.resizable(True, True)
        self._al_guardar = al_guardar
        self._nombre_sugerido = nombre_sugerido
        self._ruta_origen = ruta_origen

        marco = ttk.Frame(self)
        marco.pack(fill="both", expand=True, padx=10, pady=(10, 4))

        self.texto = tk.Text(
            marco, wrap="none", undo=editable,
            font=(FUENTES["codigo"], 10),
            bg=COLORES["blanco"], fg=COLORES["texto"],
            insertbackground=COLORES["rosa_oscuro"],
            selectbackground=COLORES["rosa_claro"],
            selectforeground=COLORES["texto"],
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=COLORES["rosa_borde"], padx=10, pady=8,
        )
        scroll_y = ttk.Scrollbar(marco, orient="vertical",
                                 command=self.texto.yview)
        scroll_x = ttk.Scrollbar(marco, orient="horizontal",
                                 command=self.texto.xview)
        self.texto.configure(yscrollcommand=scroll_y.set,
                             xscrollcommand=scroll_x.set)
        self.texto.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        self.texto.insert("1.0", contenido)
        if not editable:
            self.texto.configure(state="disabled")

        # ------------------------------------------------------------
        # Si el contenido ya está en un archivo real, mostrar su ruta.
        # ------------------------------------------------------------
        if ruta_origen:
            fila_ruta = ttk.Frame(self)
            fila_ruta.pack(fill="x", padx=10, pady=(0, 4))
            ttk.Label(
                fila_ruta,
                **con_icono(f"📁  Ya guardado en: {ruta_origen}")
            ).pack(side="left")
            ttk.Button(fila_ruta, text="Abrir carpeta",
                      command=self._abrir_carpeta_origen).pack(side="right")

        # ------------------------------------------------------------
        # Barra inferior: Guardar como... (siempre) y Guardar (si es
        # editable, para sobrescribir el archivo original, ej. lexer.l).
        # ------------------------------------------------------------
        barra = ttk.Frame(self)
        barra.pack(fill="x", padx=10, pady=(0, 10))

        self._etiqueta_estado = ttk.Label(barra, text="")
        self._etiqueta_estado.pack(side="left")

        ttk.Button(barra, **con_icono("💾  Guardar como..."),
                  command=self._guardar_como).pack(side="right")
        if editable:
            ttk.Button(barra, **con_icono("💾  Guardar"), command=self._guardar
                      ).pack(side="right", padx=(0, 6))

    def _guardar(self):
        contenido = self.texto.get("1.0", "end-1c")
        if self._al_guardar:
            self._al_guardar(contenido)
        self._mostrar_estado("Guardado ✓")

    def _guardar_como(self):
        ruta = filedialog.asksaveasfilename(
            parent=self,
            title="Guardar como",
            initialfile=self._nombre_sugerido,
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"),
                      ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return
        try:
            contenido = self.texto.get("1.0", "end-1c")
            with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                f.write(contenido)
            self._mostrar_estado(f"Guardado en {ruta} ✓")
        except OSError as e:
            messagebox.showerror("Error al guardar", str(e), parent=self)

    def _abrir_carpeta_origen(self):
        if not self._ruta_origen:
            return
        carpeta = os.path.dirname(self._ruta_origen)
        try:
            if platform.system() == "Windows":
                os.startfile(carpeta)  # noqa: S606 - accion pedida por el usuario
            elif platform.system() == "Darwin":
                subprocess.run(["open", carpeta], check=False)
            else:
                subprocess.run(["xdg-open", carpeta], check=False)
        except OSError as e:
            messagebox.showerror("No se pudo abrir la carpeta", str(e),
                                 parent=self)

    def _mostrar_estado(self, texto):
        self._etiqueta_estado.config(**con_icono(texto))
        self.after(2500, lambda: self._etiqueta_estado.config(
            **con_icono("")))
