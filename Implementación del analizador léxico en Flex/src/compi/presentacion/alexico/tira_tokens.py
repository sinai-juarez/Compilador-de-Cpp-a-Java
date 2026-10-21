"""Presentación de la tira de tokens."""

import tkinter as tk
from tkinter import ttk

from .tabla_base import crear_tabla


class TiraTokens(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        marco, self.tabla = crear_tabla(
            self, ("numero", "linea", "columna", "lexema", "token"),
            ("#", "Línea", "Columna", "Lexema", "Token"), (55, 70, 80, 280, 500),
        )
        marco.pack(fill="both", expand=True)

    def mostrar(self, tokens):
        self.limpiar()
        for i, token in enumerate(tokens, 1):
            self.tabla.insert(
                "", tk.END,
                values=(i, token.linea, token.columna, token.lexema,
                        self._token_mostrado(token)),
            )

    def limpiar(self):
        self.tabla.delete(*self.tabla.get_children())

    @staticmethod
    def _token_mostrado(token):
        return token_mostrado(token)


# Tokens que llevan su valor: tipo.valor (id además entre comillas).
_TOKENS_CON_VALOR = {
    "IDENTIFICADOR": ("id", '"'),
    "NINT": ("nint", ""),
    "NFLOAT": ("nfloat", ""),
    "STRING": ("literal", ""),
    "CARACTER": ("literal", ""),
}


def token_mostrado(token):
    """Texto de la columna Token, igual que en el analizador en Flex.

    Palabras reservadas, operadores y delimitadores: el propio lexema
    (int -> int, = -> =). Identificadores: id."a". Números: nint.1,
    nfloat.3.14. Cadenas y caracteres: literal."hola", literal.'x'.
    """
    nombre_token = str(token.token)
    lexema = str(token.lexema)

    if "RESERVADA" in nombre_token.upper():
        return lexema
    if nombre_token in _TOKENS_CON_VALOR:
        tipo, comillas = _TOKENS_CON_VALOR[nombre_token]
        return f"{tipo}.{comillas}{lexema}{comillas}"
    return nombre_token
