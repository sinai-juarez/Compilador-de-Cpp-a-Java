"""Integración con el analizador léxico real en Flex (Asignación 2).

A diferencia de `afd_lexico.py` / `analizador_lexico.py` (una reimplementación
del AFD en Python), este módulo cumple literalmente lo que pide la
Asignación 2: compila `lexer.l` con Flex y gcc, y ejecuta el binario
resultante sobre el programa fuente, leyendo su tira de tokens, tabla de
símbolos y tabla de errores.
"""

import os
import platform
import shutil
import subprocess
import sys

from compi import RAIZ_PROYECTO

if getattr(sys, "frozen", False):
    # Ejecutable empaquetado con PyInstaller: sys._MEIPASS es una carpeta
    # temporal de solo lectura que se borra al cerrar, así que ahí solo
    # vive el lexer.l ORIGINAL (para copiarlo la primera vez). La carpeta
    # de trabajo real (donde se compila y quedan los .txt) es "flex" al
    # lado del propio .exe, que sí es escribible y persiste entre corridas.
    _DIR_FLEX_EMPAQUETADO = os.path.join(sys._MEIPASS, "flex")
    _DIR_FLEX = os.path.join(os.path.dirname(sys.executable), "flex")
else:
    _DIR_FLEX_EMPAQUETADO = None
    # Carpeta de recursos "flex" en la raíz del proyecto.
    _DIR_FLEX = os.path.join(RAIZ_PROYECTO, "flex")


def _leer_bytes(ruta):
    if not os.path.isfile(ruta):
        return None
    with open(ruta, "rb") as f:
        return f.read()


def _preparar_carpeta_flex():
    """Copia el lexer.l empaquetado a la carpeta de trabajo junto al
    ejecutable (ver comentario arriba).

    ".lexer_original.l" guarda la versión que se copió la última vez. Si
    una versión nueva del programa trae otro lexer.l, se actualiza solo
    cuando el usuario no editó el suyo; la versión reemplazada queda
    respaldada en "lexer_anterior.l".
    """
    os.makedirs(_DIR_FLEX, exist_ok=True)
    if not _DIR_FLEX_EMPAQUETADO:
        return
    empaquetado = _leer_bytes(os.path.join(_DIR_FLEX_EMPAQUETADO, "lexer.l"))
    if empaquetado is None:
        return

    destino = os.path.join(_DIR_FLEX, "lexer.l")
    referencia = os.path.join(_DIR_FLEX, ".lexer_original.l")
    actual = _leer_bytes(destino)
    copia_previa = _leer_bytes(referencia)

    if actual is not None and actual != empaquetado:
        if copia_previa is not None and actual != copia_previa:
            return  # el usuario modificó su lexer.l: se respeta
        shutil.copyfile(destino, os.path.join(_DIR_FLEX, "lexer_anterior.l"))
    if actual != empaquetado:
        with open(destino, "wb") as f:
            f.write(empaquetado)
    if copia_previa != empaquetado:
        with open(referencia, "wb") as f:
            f.write(empaquetado)


_preparar_carpeta_flex()

DIR_FLEX = _DIR_FLEX  # carpeta de trabajo, expuesta para la interfaz
RUTA_LEXER_L = os.path.join(_DIR_FLEX, "lexer.l")
RUTA_LEX_YY_C = os.path.join(_DIR_FLEX, "lex.yy.c")
RUTA_TIRA_TOKENS = os.path.join(_DIR_FLEX, "tiraTokens.txt")
RUTA_ERRORES = os.path.join(_DIR_FLEX, "errores.txt")
RUTA_TABLA_SIMBOLOS = os.path.join(_DIR_FLEX, "tablaSimbolos.txt")
RUTA_FUENTE_TEMPORAL = os.path.join(_DIR_FLEX, "_fuente_actual.cpp")

_ES_WINDOWS = platform.system() == "Windows"
_NOMBRE_EJECUTABLE = "analizador_lexico.exe" if _ES_WINDOWS else "analizador_lexico"
RUTA_EJECUTABLE = os.path.join(_DIR_FLEX, _NOMBRE_EJECUTABLE)

MARCADOR_TABLA_SIMBOLOS = "Tabla de simbolos"


class ErrorFlex(Exception):
    """Fallo al compilar o ejecutar el analizador de Flex."""


# Herramientas integradas: el .exe de Windows trae su propio flex
# (win_flex, de WinFlexBison) y un compilador de C portátil (TinyCC), así
# que no hace falta instalar nada. Si no vienen integradas, se usan las
# del sistema (flex y gcc en el PATH).
_DIR_HERRAMIENTAS = os.path.join(RAIZ_PROYECTO, "herramientas")
_FLEX_INTEGRADO = os.path.join(_DIR_HERRAMIENTAS, "flex", "win_flex.exe")
_CC_INTEGRADO = os.path.join(_DIR_HERRAMIENTAS, "tcc", "tcc.exe")


def _comando_flex():
    """Comando para correr flex, o None si no hay ninguno."""
    if _ES_WINDOWS and os.path.isfile(_FLEX_INTEGRADO):
        # --wincompat: lex.yy.c usa <io.h> en lugar de <unistd.h>
        return [_FLEX_INTEGRADO, "--wincompat"]
    if shutil.which("flex"):
        return ["flex"]
    if _ES_WINDOWS and shutil.which("win_flex"):
        return ["win_flex", "--wincompat"]
    return None


def _comando_cc():
    """Comando del compilador de C, o None si no hay ninguno."""
    if _ES_WINDOWS and os.path.isfile(_CC_INTEGRADO):
        return [_CC_INTEGRADO]
    if shutil.which("gcc"):
        return ["gcc"]
    return None


def herramientas_disponibles():
    """(flex_ok, gcc_ok): si hay flex y compilador de C (integrados o en el PATH)."""
    return (_comando_flex() is not None, _comando_cc() is not None)


def _correr(comando):
    """Ejecuta un comando en la carpeta Flex y regresa su resultado.

    La salida se lee como UTF-8 (así la escribe el programa en C), y en
    Windows no se abre la ventana negra de consola por cada comando.
    """
    opciones = {}
    if _ES_WINDOWS:
        opciones["creationflags"] = subprocess.CREATE_NO_WINDOW
    return subprocess.run(
        comando, cwd=_DIR_FLEX, capture_output=True,
        text=True, encoding="utf-8", errors="replace", **opciones,
    )


def _mostrar(comando):
    """Comando legible para la ventana de resultados (sin rutas largas)."""
    return "$ " + " ".join([os.path.splitext(os.path.basename(comando[0]))[0]] + comando[1:])


def leer_lexer_l():
    with open(RUTA_LEXER_L, "r", encoding="utf-8") as f:
        return f.read()


def guardar_lexer_l(contenido):
    with open(RUTA_LEXER_L, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)


def compilar():
    """Ejecuta flex sobre lexer.l y luego compila lex.yy.c con gcc (o
    con TinyCC, el compilador integrado en el .exe de Windows).

    Devuelve el texto combinado de ambos comandos si todo sale bien.
    Lanza ErrorFlex (con la salida de los comandos, o un mensaje sobre
    herramientas faltantes) si algo falla.
    """
    cmd_flex, cmd_cc = _comando_flex(), _comando_cc()
    faltantes = [n for n, c in (("flex", cmd_flex), ("gcc", cmd_cc)) if c is None]
    if faltantes:
        raise ErrorFlex(
            "No se encontraron en el PATH: " + ", ".join(faltantes) + ".\n\n"
            "Instala Flex y un compilador de C y agrega su carpeta 'bin' "
            "al PATH.\nEn Windows: MinGW-w64 (gcc) + WinFlexBison "
            "(flex); en Ubuntu/Debian: sudo apt install flex gcc."
        )

    if not os.path.isfile(RUTA_LEXER_L):
        raise ErrorFlex(f"No se encontró {RUTA_LEXER_L}")

    salida = []
    for comando in (cmd_flex + ["lexer.l"],
                    cmd_cc + ["-o", _NOMBRE_EJECUTABLE, "lex.yy.c"]):
        resultado = _correr(comando)
        salida.append(_mostrar(comando) + "\n" + resultado.stdout + resultado.stderr)
        if resultado.returncode != 0:
            raise ErrorFlex("\n".join(salida))

    return "\n".join(salida).strip() or "Compilación exitosa."


def ejecutar(codigo_fuente):
    """Corre el ejecutable ya compilado sobre `codigo_fuente` (texto).

    Escribe el código en un archivo temporal dentro de la carpeta Flex,
    invoca al ejecutable con ese archivo y regresa
    (tira_tokens, tabla_simbolos, errores) como texto plano, tal cual
    los produce el programa en C (mismo formato que verían en consola).

    Lanza ErrorFlex si el ejecutable no existe todavía o si truena al
    correr.
    """
    if not os.path.isfile(RUTA_EJECUTABLE):
        raise ErrorFlex(
            "El analizador léxico en Flex todavía no se ha compilado.\n"
            "Presiona primero el botón 'Compilar'."
        )
    if (os.path.isfile(RUTA_LEXER_L)
            and os.path.getmtime(RUTA_LEXER_L) > os.path.getmtime(RUTA_EJECUTABLE)):
        raise ErrorFlex(
            "lexer.l cambió después de la última compilación.\n"
            "Presiona 'Compilar' para que el analizador use la versión nueva."
        )

    with open(RUTA_FUENTE_TEMPORAL, "w", encoding="utf-8", newline="\n") as f:
        f.write(codigo_fuente)

    resultado = _correr(
        [os.path.abspath(RUTA_EJECUTABLE), os.path.abspath(RUTA_FUENTE_TEMPORAL)]
    )

    if resultado.returncode != 0 and not resultado.stdout:
        raise ErrorFlex(
            "El analizador léxico terminó con un error:\n\n" + resultado.stderr
        )

    # La tabla de símbolos va al final de la consola, precedida por una
    # línea "Tabla de simbolos" (se busca la última, por si el programa
    # fuente trae ese mismo texto dentro de una cadena).
    marcador = "\n" + MARCADOR_TABLA_SIMBOLOS + "\n"
    if marcador in resultado.stdout:
        tira, _, resto = resultado.stdout.rpartition(marcador)
        simbolos_consola = MARCADOR_TABLA_SIMBOLOS + "\n" + resto
    else:
        tira, simbolos_consola = resultado.stdout, ""

    # Se prefiere siempre leer los .txt que el propio ejecutable en C
    # escribió en disco (ver main() en lexer.l); son la fuente real que
    # pide la Asignación 2. Si vinieran de un .exe viejo compilado antes
    # de tablaSimbolos.txt, se usa lo impreso en consola como respaldo.
    tira_tokens = _leer_si_existe(RUTA_TIRA_TOKENS)
    if tira_tokens is None:
        tira_tokens = tira.strip()

    simbolos = _leer_si_existe(RUTA_TABLA_SIMBOLOS)
    if simbolos is None:
        simbolos = simbolos_consola.strip()

    errores = _leer_si_existe(RUTA_ERRORES) or "(sin errores léxicos)"

    return tira_tokens, simbolos.strip() or "(sin identificadores)", errores


def _leer_si_existe(ruta):
    if os.path.isfile(ruta):
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    return None
