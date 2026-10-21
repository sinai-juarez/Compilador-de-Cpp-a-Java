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
# Categorías tal como las nombra la especificación léxica
# (expresiones_regulares.pdf, sección 3). Cada categoría se reconoce
# como un token distinto (RESERVADA_<categoria>) en vez de un único
# "PALABRA_RESERVADA" genérico, igual que en el analizador en Flex.

TIPO_DATO = {"int", "float", "double", "char", "bool", "void", "string"}
CONTROL = {
    "if", "else", "switch", "case", "default", "while", "do", "for",
    "break", "continue", "return",
}
LOGICO_BOOLEANO = {"true", "false"}
PRINCIPAL = {"main"}
MODIFICADOR_TIPO = {"short", "long", "signed", "unsigned", "const", "static"}
ESTRUCTURA_OBJETO = {
    "struct", "class", "enum", "public", "private", "protected",
}
OPERADOR_PALABRA = {"new", "delete", "sizeof", "typedef"}
ESPACIO_NOMBRES = {"using", "namespace"}
SALIDA_TEXTO = {"cin", "cout", "endl", "std", "printf", "scanf"}

# Orden de búsqueda -> nombre de token. El nombre siempre contiene
# "RESERVADA" para que la interfaz (ui/tira_tokens.py) siga mostrando
# solo el lexema en la columna Token (ej. "int", no "RESERVADA_TIPO_DATO.int").
_CATEGORIAS_RESERVADAS = (
    (TIPO_DATO, "RESERVADA_TIPO_DATO"),
    (CONTROL, "RESERVADA_CONTROL"),
    (LOGICO_BOOLEANO, "RESERVADA_LOGICO_BOOLEANO"),
    (PRINCIPAL, "RESERVADA_PRINCIPAL"),
    (MODIFICADOR_TIPO, "RESERVADA_MODIFICADOR_TIPO"),
    (ESTRUCTURA_OBJETO, "RESERVADA_ESTRUCTURA_OBJETO"),
    (OPERADOR_PALABRA, "RESERVADA_OPERADOR_PALABRA"),
    (ESPACIO_NOMBRES, "RESERVADA_ESPACIO_NOMBRES"),
    (SALIDA_TEXTO, "RESERVADA_SALIDA_TEXTO"),
)

PALABRAS_RESERVADAS = set().union(*(grupo for grupo, _ in _CATEGORIAS_RESERVADAS))


def categoria_palabra_reservada(lexema: str) -> str:
    """Token específico de una palabra reservada (ej. "int" -> "RESERVADA_TIPO_DATO").

    Solo debe llamarse con un lexema que ya se sabe que está en
    PALABRAS_RESERVADAS.
    """
    for grupo, nombre_token in _CATEGORIAS_RESERVADAS:
        if lexema in grupo:
            return nombre_token
    return "PALABRA_RESERVADA"
