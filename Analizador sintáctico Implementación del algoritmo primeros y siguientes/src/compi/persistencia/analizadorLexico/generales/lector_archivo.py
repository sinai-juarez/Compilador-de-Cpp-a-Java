class LectorArchivo:
    """Carga programas fuente desde archivos C/C++."""

    def cargar_archivo(self, ruta_archivo: str) -> str:
        with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as archivo:
            return archivo.read()
