"""Clases Gramatica y LectorGramatica.

Formato del archivo de la gramática (como en la Asignación 3):

    E T F              <- línea 1: símbolos no terminales
    + * ( ) id         <- línea 2: símbolos terminales
    E                  <- línea 3 (opcional): símbolo inicial; si no se
                          escribe, el inicial es el primer no terminal
    E→E+T              <- después, una regla de producción por línea
    E→T
    ...

- La flecha puede escribirse como "→", "->" o "::=".
- Se permiten alternativas con "|":  F → ( E ) | id
  salvo que "|" esté declarado como terminal (como en las gramáticas de
  C++, donde | y || son operadores); entonces va una regla por línea.
- La línea de terminales puede contener "->" (operador de C++): una línea
  solo es regla si tiene un único símbolo antes de la flecha.
- La cadena vacía se escribe "ε", "eps", "epsilon" o "λ" (o con el lado
  derecho vacío).
- Los símbolos pueden ir separados por espacios o juntos (E→E+T): en ese
  caso se reconocen por coincidencia más larga con los símbolos declarados.
- Gramática aumentada: la primera regla puede ser S' → S $ sin declarar S'
  ni $ en el encabezado (como en el ejemplo de la Asignación 4); entonces
  S' es el símbolo inicial y $ se agrega a los terminales.
- Las líneas que empiezan con "//" son comentarios.
- Si se omiten las líneas 1 y 2, los no terminales se deducen de los lados
  izquierdos y el resto son terminales; entonces los símbolos del lado
  derecho deben ir separados por espacios.
"""

EPSILON = "ε"
FIN = "$"
FLECHAS = ("→", "->", "::=")
ALIAS_EPSILON = {"ε", "eps", "epsilon", "λ", "''"}
_COMILLAS = {"’": "'", "‘": "'", "´": "'", "′": "'"}


class ErrorGramatica(Exception):
    """Error de formato en el archivo de la gramática."""


class Gramatica:
    """G = (no terminales, terminales, símbolo inicial, producciones).

    Cada producción es una tupla (A, (Y1, Y2, ..., Yk)); la producción
    A → ε se guarda con el lado derecho vacío: (A, ()).
    """

    def __init__(self, no_terminales, terminales, inicial, producciones):
        self.no_terminales = list(no_terminales)
        self.terminales = list(terminales)
        self.inicial = inicial
        self.producciones = list(producciones)

    def es_no_terminal(self, simbolo):
        return simbolo in self.no_terminales

    def es_terminal(self, simbolo):
        return simbolo in self.terminales

    def __str__(self):
        lineas = [" ".join(self.no_terminales), " ".join(self.terminales)]
        for izq, der in self.producciones:
            lineas.append(f"{izq} → {' '.join(der) if der else EPSILON}")
        return "\n".join(lineas)


class LectorGramatica:
    """Lee una gramática libre de contexto desde un archivo o un texto."""

    def cargar_archivo(self, ruta):
        with open(ruta, "r", encoding="utf-8", errors="ignore") as archivo:
            return archivo.read()

    def leer_archivo(self, ruta):
        return self.leer(self.cargar_archivo(ruta))

    def leer(self, texto):
        lineas = []
        for num, linea in enumerate(texto.splitlines(), 1):
            linea = _normalizar(linea).strip()
            if linea and not linea.startswith("//"):
                lineas.append((num, linea))
        if not lineas:
            raise ErrorGramatica("La gramática está vacía.")

        # Las líneas antes de la primera regla (A → α) son el encabezado.
        i = 0
        while i < len(lineas) and not _es_regla(lineas[i][1]):
            i += 1
        encabezado, reglas = lineas[:i], lineas[i:]
        if not reglas:
            raise ErrorGramatica(
                "No se encontraron reglas de producción (A → α).")

        if not encabezado:
            return self._leer_sin_encabezado(reglas)
        if len(encabezado) not in (2, 3):
            raise ErrorGramatica(
                f"Línea {encabezado[0][0]}: antes de las reglas se esperan "
                "2 líneas (no terminales y terminales) y, opcionalmente, una "
                f"tercera con el símbolo inicial; se encontraron "
                f"{len(encabezado)}.")
        return self._leer_con_encabezado(encabezado, reglas)

    # ------------------------------------------------------------------

    def _leer_con_encabezado(self, encabezado, reglas):
        no_terminales = _sin_repetidos(encabezado[0][1].split())
        terminales = [t for t in _sin_repetidos(encabezado[1][1].split())
                      if t not in ALIAS_EPSILON]

        comunes = [s for s in no_terminales if s in terminales]
        if comunes:
            raise ErrorGramatica(
                "Estos símbolos están declarados como no terminales y "
                f"como terminales a la vez: {' '.join(comunes)}")

        if len(encabezado) == 3:
            num, linea = encabezado[2]
            inicial = linea.split()[0]
            if inicial not in no_terminales:
                raise ErrorGramatica(
                    f"Línea {num}: el símbolo inicial «{inicial}» no está "
                    "entre los no terminales.")
        else:
            inicial = no_terminales[0]

        # Gramática aumentada (Asignación 4): la primera regla puede ser
        # S' → S $ aunque S' y $ no estén declarados en el encabezado.
        izq_primera, der_primera = _partir_regla(*reglas[0])
        if izq_primera not in no_terminales and der_primera.endswith(FIN):
            no_terminales.insert(0, izq_primera)
            if len(encabezado) == 2:
                inicial = izq_primera
        if FIN not in terminales and any(
                FIN in _partir_regla(num, linea)[1] for num, linea in reglas):
            terminales.append(FIN)

        # Más largos primero, para la coincidencia más larga (E' antes que E).
        simbolos = sorted(no_terminales + terminales, key=len, reverse=True)
        separar_alternativas = "|" not in terminales
        producciones = []
        for num, linea in reglas:
            izq, der = _partir_regla(num, linea)
            if izq not in no_terminales:
                raise ErrorGramatica(
                    f"Línea {num}: «{izq}» está del lado izquierdo pero no "
                    "está declarado como no terminal.")
            alternativas = der.split("|") if separar_alternativas else [der]
            for alternativa in alternativas:
                producciones.append(
                    (izq, _tokenizar(alternativa, simbolos, num)))

        _validar_producciones(no_terminales, producciones)
        return Gramatica(no_terminales, terminales, inicial, producciones)

    def _leer_sin_encabezado(self, reglas):
        partes = []
        no_terminales = []
        for num, linea in reglas:
            izq, der = _partir_regla(num, linea)
            if not izq or " " in izq:
                raise ErrorGramatica(
                    f"Línea {num}: el lado izquierdo debe ser un solo "
                    "no terminal.")
            if izq not in no_terminales:
                no_terminales.append(izq)
            partes.append((izq, der))

        producciones = []
        terminales = []
        for izq, der in partes:
            for alternativa in der.split("|"):
                simbolos = tuple(s for s in alternativa.split()
                                 if s not in ALIAS_EPSILON)
                for s in simbolos:
                    if s not in no_terminales and s not in terminales:
                        terminales.append(s)
                producciones.append((izq, simbolos))

        return Gramatica(no_terminales, terminales, no_terminales[0],
                         producciones)


# ----------------------------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------------------------

def _normalizar(linea):
    for original, reemplazo in _COMILLAS.items():
        linea = linea.replace(original, reemplazo)
    return linea


def _buscar_flecha(linea):
    """Devuelve (posición, flecha) de la primera flecha, o None."""
    encontradas = [(linea.find(f), f) for f in FLECHAS if f in linea]
    return min(encontradas) if encontradas else None


def _es_regla(linea):
    """Una regla tiene un solo símbolo antes de la flecha. Así la línea de
    terminales no se confunde con una regla aunque contenga "->" (el
    operador de acceso a miembro de C++)."""
    flecha = _buscar_flecha(linea)
    return flecha is not None and len(linea[:flecha[0]].split()) == 1


def _partir_regla(num, linea):
    flecha = _buscar_flecha(linea)
    if flecha is None:
        raise ErrorGramatica(
            f"Línea {num}: falta la flecha (→ o ->) en «{linea}».")
    pos, texto_flecha = flecha
    izq = linea[:pos].strip()
    if not izq:
        raise ErrorGramatica(f"Línea {num}: falta el lado izquierdo.")
    return izq, linea[pos + len(texto_flecha):].strip()


def _tokenizar(alternativa, simbolos, num):
    """Convierte el lado derecho en una tupla de símbolos declarados."""
    resultado = []
    for trozo in alternativa.split():
        if trozo in ALIAS_EPSILON:
            continue
        pos = 0
        while pos < len(trozo):
            for simbolo in simbolos:
                if trozo.startswith(simbolo, pos):
                    resultado.append(simbolo)
                    pos += len(simbolo)
                    break
            else:
                if trozo[pos] == EPSILON:
                    pos += 1
                    continue
                raise ErrorGramatica(
                    f"Línea {num}: «{trozo[pos:]}» no es un símbolo "
                    "declarado (revisa las líneas de terminales y no "
                    "terminales).")
    return tuple(resultado)


def _validar_producciones(no_terminales, producciones):
    con_reglas = {izq for izq, _ in producciones}
    sin_reglas = [a for a in no_terminales if a not in con_reglas]
    if sin_reglas:
        raise ErrorGramatica(
            "Estos no terminales no tienen reglas de producción: "
            + " ".join(sin_reglas))


def _sin_repetidos(elementos):
    return list(dict.fromkeys(elementos))
