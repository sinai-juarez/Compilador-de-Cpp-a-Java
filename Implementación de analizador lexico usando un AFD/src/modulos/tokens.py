# ============================================================
# TOKEN LÉXICO
# ============================================================

class TokenLexico:

    def __init__(
        self,
        linea: int,
        columna: int,
        token: str,
        lexema: str,
        valorLexico: str
    ):
        self.linea = linea
        self.columna = columna
        self.token = token
        self.lexema = lexema
        self.valorLexico = valorLexico

    def __str__(self) -> str:
        return (
            f"TokenLexico("
            f"linea={self.linea}, "
            f"columna={self.columna}, "
            f"token='{self.token}', "
            f"lexema='{self.lexema}', "
            f"valorLexico='{self.valorLexico}')"
        )

# ============================================================
# ERROR LÉXICO
# ============================================================

class ErrorLexico:

    def __init__(
        self,
        linea: int,
        columna: int,
        caracter: str,
        mensaje: str
    ):
        self.linea = linea
        self.columna = columna
        self.caracter = caracter
        self.mensaje = mensaje

    def __str__(self) -> str:
        return (
            f"ErrorLexico("
            f"linea={self.linea}, "
            f"columna={self.columna}, "
            f"caracter='{self.caracter}', "
            f"mensaje='{self.mensaje}')"
        )

# ============================================================
# PALABRAS RESERVADAS
# ============================================================

PALABRAS_RESERVADAS = {
    # Tipos de dato
    "int", "float", "double", "char", "bool", "void", "string",
    "short", "long", "signed", "unsigned",
    # Control de flujo
    "if", "else", "switch", "case", "default", "while", "do", "for",
    "break", "continue", "return",
    # Literales y función principal
    "true", "false", "main",
    # Modificadores y declaraciones
    "const", "static", "struct", "class", "enum", "typedef",
    "public", "private", "protected",
    # Operadores de memoria y espacios de nombres
    "new", "delete", "sizeof", "using", "namespace",
    # Entrada y salida estándar
    "cin", "cout", "endl",
}
