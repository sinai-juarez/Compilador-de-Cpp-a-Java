"""Clase VentanaALexico: pantalla del analizador léxico basado en el AFD."""

from tkinter import messagebox

from compi.persistencia.analizadorLexico.alexico.afd_lexico import AFDAlexico
from compi.persistencia.analizadorLexico.alexico.analizador_lexico import AnalizadorLexico
from .pantalla_analizador import PantallaAnalizador
from .ventana_resultados import abrir_ventanas_resultados


class VentanaALexico(PantallaAnalizador):

    def __init__(self, padre):
        super().__init__(padre, "✿  ANALIZADOR LÉXICO (AFD)  ✿")
        self.analizador = None
        self._ventanas_resultado = []
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

            # Como en Flex: cada salida en su propia subventana.
            self._cerrar_ventanas()
            self._ventanas_resultado, total_simbolos = (
                abrir_ventanas_resultados(self.padre.root, tokens, errores))
            self.padre.mostrar_estado(
                f"♡  Análisis terminado: {len(tokens)} tokens, "
                f"{total_simbolos} símbolos y {len(errores)} errores.")

        except Exception as e:
            messagebox.showerror(
                "Error durante el análisis", f"{type(e).__name__}: {e}")

    def cerrar_resultados(self):
        self.analizador = None
        self._cerrar_ventanas()

    def _cerrar_ventanas(self):
        for v in self._ventanas_resultado:
            if v.winfo_exists():
                v.destroy()
        self._ventanas_resultado = []
