import os
import sys

from afd_lexico import AFDAlexico
from analizador_lexico import AnalizadorLexico
from lector_archivo import LectorArchivo

_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PRUEBA = os.path.join(_DIR, "..", "..", "archivos_prueba", "prueba.cpp")


def imprimir_resultados(ruta, tokens, errores):
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  ANALISIS LEXICO: {ruta}")
    print(sep)

    print(f"\n{'[ TOKENS ENCONTRADOS ]':^60}")
    print("-" * 60)
    if tokens:
        for tk in tokens:
            print(tk)
    else:
        print("  (ninguno)")

    print(f"\n{'[ ERRORES LEXICOS ]':^60}")
    print("-" * 60)
    if errores:
        for err in errores:
            print(err)
    else:
        print("  No se encontraron errores lexicos.")

    print(f"\n  Total tokens : {len(tokens)}")
    print(f"  Total errores: {len(errores)}")
    print(sep)


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_PRUEBA

    codigo = LectorArchivo().cargar_archivo(ruta)
    analizador = AnalizadorLexico(codigo, AFDAlexico())
    tokens = analizador.analizar()

    imprimir_resultados(ruta, tokens, analizador.errores)


if __name__ == "__main__":
    main()
