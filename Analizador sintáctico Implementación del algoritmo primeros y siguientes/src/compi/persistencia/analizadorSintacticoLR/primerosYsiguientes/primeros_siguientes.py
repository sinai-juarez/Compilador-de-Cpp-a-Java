"""Clase PrimerosSiguientes: cálculo de los conjuntos PRIMERO y SIGUIENTE.

Implementa los algoritmos de la Asignación 3 (Tema 3, Análisis sintáctico).

PRIMERO(X), para todo símbolo gramatical X; se aplican las reglas hasta
que no se puedan añadir más terminales o ε a ningún conjunto:
    1. Si X es terminal, PRIMERO(X) = {X}.
    2. Si X → ε, añadir ε a PRIMERO(X).
    3. Si X → Y1 Y2 ... Yk, añadir PRIMERO(Y1) excepto ε; si Y1 ⇒ ε,
       añadir también PRIMERO(Y2), y así sucesivamente. Si ε está en
       PRIMERO(Yj) para j = 1..k, añadir ε a PRIMERO(X).

SIGUIENTE(A), para todo no terminal A; se aplican las reglas hasta que no
se pueda agregar nada más a ningún conjunto:
    1. Colocar $ en SIGUIENTE(S), donde S es el símbolo inicial.
    2. Si existe B → αAβ, SIGUIENTE(A) ← PRIMERO(β) excepto ε.
    3. Si existe B → αA, o B → αAβ con ε en PRIMERO(β),
       SIGUIENTE(A) ← SIGUIENTE(B).
"""

from compi.persistencia.analizadorSintacticoLR.generales.gramatica import EPSILON, FIN


class PrimerosSiguientes:

    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.primeros = {}
        self.siguientes = {}

    def calcular(self):
        self.calcular_primeros()
        self.calcular_siguientes()
        return self

    # ------------------------------------------------------------------
    # PRIMEROS
    # ------------------------------------------------------------------

    def calcular_primeros(self):
        g = self.gramatica
        # Regla 1: PRIMERO(a) = {a} para todo terminal a.
        self.primeros = {t: {t} for t in g.terminales}
        for a in g.no_terminales:
            self.primeros[a] = set()

        cambio = True
        while cambio:
            cambio = False
            for x, derecha in g.producciones:
                # Reglas 2 y 3: si derecha es vacía, primeros_de devuelve {ε}.
                nuevos = self.primeros_de(derecha) - self.primeros[x]
                if nuevos:
                    self.primeros[x] |= nuevos
                    cambio = True
        return self.primeros

    def primeros_de(self, simbolos):
        """PRIMERO de una cadena Y1 Y2 ... Yk (regla 3)."""
        resultado = set()
        for y in simbolos:
            resultado |= self.primeros[y] - {EPSILON}
            if EPSILON not in self.primeros[y]:
                return resultado
        # Todos los Yj derivan ε (o la cadena es vacía).
        resultado.add(EPSILON)
        return resultado

    # ------------------------------------------------------------------
    # SIGUIENTES
    # ------------------------------------------------------------------

    def calcular_siguientes(self):
        g = self.gramatica
        self.siguientes = {a: set() for a in g.no_terminales}
        # Regla 1.
        self.siguientes[g.inicial].add(FIN)

        cambio = True
        while cambio:
            cambio = False
            for b, derecha in g.producciones:
                for i, a in enumerate(derecha):
                    if not g.es_no_terminal(a):
                        continue
                    primeros_beta = self.primeros_de(derecha[i + 1:])
                    # Regla 2.
                    nuevos = primeros_beta - {EPSILON}
                    # Regla 3 (β vacía o β ⇒ ε).
                    if EPSILON in primeros_beta:
                        nuevos |= self.siguientes[b]
                    nuevos -= self.siguientes[a]
                    if nuevos:
                        self.siguientes[a] |= nuevos
                        cambio = True
        return self.siguientes

    # ------------------------------------------------------------------
    # SALIDAS
    # ------------------------------------------------------------------

    # Los conjuntos ya están completos; lo siguiente solo decide en qué
    # orden se muestran sus elementos: el orden en que se agregan al
    # aplicar las reglas recorriendo las producciones de arriba hacia
    # abajo, como en el ejemplo del PDF (S(T)={ $ + ) * }).

    def _orden_primeros(self, x, visitando):
        if not self.gramatica.es_no_terminal(x):
            return [x]
        orden = []
        for izq, derecha in self.gramatica.producciones:
            if izq == x:
                orden += self._orden_cadena(derecha, visitando | {x})
        return _completar(orden, self.primeros[x])

    def _orden_cadena(self, simbolos, visitando):
        orden = []
        for y in simbolos:
            if y not in visitando:
                orden += [s for s in self._orden_primeros(y, visitando)
                          if s != EPSILON]
            if EPSILON not in self.primeros[y]:
                return orden
        return orden + [EPSILON]

    def _orden_siguientes(self, a, visitando):
        g = self.gramatica
        orden = [FIN] if a == g.inicial else []
        for b, derecha in g.producciones:
            for i, simbolo in enumerate(derecha):
                if simbolo != a:
                    continue
                beta = derecha[i + 1:]
                orden += [s for s in self._orden_cadena(beta, set())
                          if s != EPSILON]
                if (EPSILON in self.primeros_de(beta)
                        and b not in visitando | {a}):
                    orden += self._orden_siguientes(b, visitando | {a})
        return _completar(orden, self.siguientes[a])

    def formatear(self, elementos):
        return "{ " + " ".join(elementos) + " }"

    def lineas_primeros(self):
        return [f"P({a})={self.formatear(self._orden_primeros(a, set()))}"
                for a in self.gramatica.no_terminales]

    def lineas_siguientes(self):
        return [f"S({a})="
                f"{self.formatear(self._orden_siguientes(a, set()))}"
                for a in self.gramatica.no_terminales]

    def reporte(self):
        """Salida en el mismo formato que el ejemplo de la asignación."""
        return "\n".join(["PRIMEROS", *self.lineas_primeros(),
                          "SIGUIENTES", *self.lineas_siguientes()])


def _completar(orden, conjunto):
    """Quita repetidos y agrega al final lo que falte del conjunto (los
    elementos que llegan por recursión, ej. E → E + T)."""
    resultado = [s for s in dict.fromkeys(orden) if s in conjunto]
    return resultado + sorted(conjunto - set(resultado))
