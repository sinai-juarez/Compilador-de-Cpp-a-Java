"""Presentación de la tira de tokens."""

import tkinter as tk
from tkinter import ttk

from .tabla_base import crear_tabla


class TiraTokens(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        marco, self.tabla = crear_tabla(
            self, ("numero", "linea", "lexema", "token"),
            ("#", "Línea", "Lexema", "Token"), (55, 80, 280, 500),
        )
        marco.pack(fill="both", expand=True)

    def mostrar(self, tokens):
        self.limpiar()
        for i, token in enumerate(tokens, 1):
            self.tabla.insert(
                "", tk.END,
                values=(i, token.linea, token.lexema,
                        self._token_mostrado(token)),
            )

    def limpiar(self):
        self.tabla.delete(*self.tabla.get_children())

    @staticmethod
    def _token_mostrado(token):
        """Texto de la columna Token.

        Palabras reservadas: igual que el lexema (float -> float).
        Identificadores: ID.lexema. Demás tokens: TOKEN.VALOR_LEXICO, o solo
        TOKEN cuando coincide con el valor léxico.
        """
        nombre_token = str(token.token)
        valor_lexico = str(token.valorLexico)

        if "RESERVADA" in nombre_token.upper():
            return str(token.lexema)
        if nombre_token == "IDENTIFICADOR":
            return "ID." + str(token.lexema)
        if nombre_token == valor_lexico:
            return nombre_token
        return nombre_token + "." + valor_lexico
