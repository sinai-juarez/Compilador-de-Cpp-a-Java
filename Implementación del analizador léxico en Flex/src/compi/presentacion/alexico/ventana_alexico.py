"""Clase VentanaALexico: pantalla del analizador léxico basado en el AFD."""

from tkinter import messagebox

from compi.persistencia.analizadorLexico.alexico.afd_lexico import AFDAlexico
from compi.persistencia.analizadorLexico.alexico.analizador_lexico import AnalizadorLexico
from .pantalla_analizador import PantallaAnalizador
from .ventana_resultados import VentanaResultados


class VentanaALexico(PantallaAnalizador):

    def __init__(self, padre):
        super().__init__(padre, "✿  ANALIZADOR LÉXICO (AFD)  ✿")
        self.analizador = None
        self.ventana_resultados = None
        self._crear_panel_fuente(self.analizar)
        self._crear_editor()

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
                self.ventana_resultados = VentanaResultados(self.padre.root)
            total_simbolos = self.ventana_resultados.mostrar(tokens, errores)
            self.padre.mostrar_estado(
                f"♡  Análisis terminado: {len(tokens)} tokens, "
                f"{total_simbolos} símbolos y {len(errores)} errores.")

        except Exception as e:
            messagebox.showerror(
                "Error durante el análisis", f"{type(e).__name__}: {e}")

    def cerrar_resultados(self):
        self.analizador = None
        if (self.ventana_resultados is not None
                and self.ventana_resultados.winfo_exists()):
            self.ventana_resultados.destroy()
        self.ventana_resultados = None
