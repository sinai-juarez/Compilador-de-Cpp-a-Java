"""Clase VentanaALexicoFlex: pantalla del analizador léxico en Flex.

Abre lexer.l, lo compila con flex+gcc y corre el ejecutable resultante,
que produce 3 ventanas: tira de tokens, tabla de símbolos y de errores.
"""

from tkinter import ttk, messagebox

from compi.persistencia.analizadorLexico.flex import compilador_flex
from .pantalla_analizador import PantallaAnalizador
from .ventana_texto import VentanaTexto


class VentanaALexicoFlex(PantallaAnalizador):

    def __init__(self, padre):
        super().__init__(padre, "✿  ANALIZADOR LÉXICO (FLEX)  ✿")
        self._ventana_flex_l = None
        self._ventanas_resultado = []
        self._crear_panel_fuente()
        self._crear_panel_flex()
        self._crear_editor()

    def _crear_panel_flex(self):
        panel_flex = ttk.LabelFrame(self, text="  Analizador en Flex  ")
        panel_flex.pack(fill="x", padx=18, pady=(0, 8))

        ttk.Button(panel_flex, text="📄  Abrir archivo flex",
                   command=self.abrir_archivo_flex).grid(
            row=0, column=0, padx=7, pady=10)
        ttk.Button(panel_flex, text="⚙  Compilar",
                   command=self.compilar_flex).grid(
            row=0, column=1, padx=7, pady=10)
        ttk.Button(panel_flex, text="▶  Ejecutar analizador léxico (Flex)",
                   command=self.ejecutar_flex).grid(
            row=0, column=2, padx=7, pady=10)
        ttk.Label(
            panel_flex,
            text="Usa el programa fuente cargado arriba; compila lexer.l "
                 "con flex+gcc y corre el ejecutable real."
        ).grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 8), sticky="w")

    def abrir_archivo_flex(self):
        """'Abrir archivo flex': abre lexer.l en una ventana editable."""
        if self._ventana_flex_l is not None and self._ventana_flex_l.winfo_exists():
            self._ventana_flex_l.lift()
            return
        try:
            contenido = compilador_flex.leer_lexer_l()
        except OSError as e:
            messagebox.showerror("Error al abrir lexer.l", str(e))
            return

        self._ventana_flex_l = VentanaTexto(
            self.padre.root, "lexer.l — Analizador léxico en Flex",
            contenido, editable=True,
            al_guardar=self._guardar_lexer_l)

    def _guardar_lexer_l(self, contenido):
        try:
            compilador_flex.guardar_lexer_l(contenido)
            self.padre.mostrar_estado("♡  lexer.l guardado.")
        except OSError as e:
            messagebox.showerror("Error al guardar lexer.l", str(e))

    def compilar_flex(self):
        """'Compilar': corre flex y gcc sobre lexer.l."""
        self.padre.mostrar_estado("♡  Compilando lexer.l con flex y gcc…")
        self.update_idletasks()
        try:
            salida = compilador_flex.compilar()
        except compilador_flex.ErrorFlex as e:
            self.padre.mostrar_estado("♡  La compilación falló.")
            messagebox.showerror("Error de compilación", str(e))
            return
        self.padre.mostrar_estado("♡  Compilación exitosa.")
        messagebox.showinfo("Compilación exitosa",
                            "flex + gcc terminaron sin errores.\n\n" + salida)

    def ejecutar_flex(self):
        """'Ejecutar analizador léxico': corre el ejecutable de Flex sobre
        el programa fuente cargado y abre 3 ventanas separadas con sus
        resultados (tira de tokens, tabla de símbolos, tabla de errores)."""
        codigo = self.editor.contenido()
        if not codigo.strip():
            messagebox.showwarning(
                "Analizador léxico (Flex)",
                "No hay código fuente para analizar.")
            return

        try:
            tira, simbolos, errores = compilador_flex.ejecutar(codigo)
        except compilador_flex.ErrorFlex as e:
            messagebox.showerror("Error al ejecutar el analizador", str(e))
            return

        self.cerrar_resultados()
        root = self.padre.root
        self._ventanas_resultado = [
            VentanaTexto(root, "Tira de tokens (Flex)", tira,
                         geometria="820x600+80+60",
                         nombre_sugerido="tiraTokens.txt",
                         ruta_origen=compilador_flex.RUTA_TIRA_TOKENS),
            VentanaTexto(root, "Tabla de símbolos (Flex)", simbolos,
                         geometria="420x600+920+60",
                         nombre_sugerido="tablaSimbolos.txt",
                         ruta_origen=compilador_flex.RUTA_TABLA_SIMBOLOS),
            VentanaTexto(root, "Tabla de errores (Flex)", errores,
                         geometria="820x300+80+680",
                         nombre_sugerido="errores.txt",
                         ruta_origen=compilador_flex.RUTA_ERRORES),
        ]
        self.padre.mostrar_estado(
            f"♡  Análisis en Flex terminado. Archivos en: {compilador_flex.DIR_FLEX}")

    def cerrar_resultados(self):
        for v in self._ventanas_resultado:
            if v.winfo_exists():
                v.destroy()
        self._ventanas_resultado = []
