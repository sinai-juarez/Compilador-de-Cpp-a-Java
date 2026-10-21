"""Clase ColeccionCanonica: estados del AFD LR(0) de una gramática aumentada.

Implementa los algoritmos de la Asignación 4 (Tema 3, Análisis sintáctico).

Un elemento [A → α·β] se representa con la tupla (p, k): p es el índice de
la producción A → αβ en la gramática aumentada y k la posición del punto.

coleccionCanonica(G'):
    C := {I0 := cerradura({[S' → ·S $]})}
    hacer
        para cada conjunto de elementos Ii en C
            para cada símbolo gramatical ·X de cada elemento de Ii
                si X es $ entonces Ir_a(Ii, X) := aceptación
                sino si Ir_a(Ii, X) no está vacío y no está en C entonces
                    añadir a C Ii+1 := Ir_a(Ii, X), como un nuevo estado
    mientras haya más conjuntos de elementos a añadir a C

cerradura(I):
    hacer
        para cada elemento [A → α·Bβ] en I, con B no terminal
            para cada producción B → γ
                si [B → ·γ] no está en I, añadirlo a I
    mientras haya elementos por añadir a I

Ir_a(I, X):
    J := {[A → αX·β] | [A → α·Xβ] está en I}
    return cerradura(J)
"""

from compi.persistencia.analizadorSintacticoLR.generales.gramatica import (
    EPSILON, FIN, Gramatica)

ACEPTACION = "Aceptación"
PUNTO = "·"


def aumentar(gramatica):
    """Devuelve la gramática aumentada G' (S' → S $ como producción 0).

    Si la gramática ya viene aumentada (el inicial tiene una sola
    producción S' → S $), solo se coloca esa producción en primer lugar.
    """
    g = gramatica
    del_inicial = [p for p in g.producciones if p[0] == g.inicial]
    if (len(del_inicial) == 1 and len(del_inicial[0][1]) == 2
            and del_inicial[0][1][1] == FIN
            and g.es_no_terminal(del_inicial[0][1][0])):
        resto = [p for p in g.producciones if p[0] != g.inicial]
        return Gramatica(g.no_terminales, g.terminales, g.inicial,
                         del_inicial + resto)

    # S' no debe chocar con otro símbolo (en la Gramática 6 E' ya existe).
    nuevo = g.inicial + "'"
    while nuevo in g.no_terminales or nuevo in g.terminales:
        nuevo += "'"
    terminales = g.terminales + ([FIN] if FIN not in g.terminales else [])
    return Gramatica([nuevo] + g.no_terminales, terminales, nuevo,
                     [(nuevo, (g.inicial, FIN))] + g.producciones)


class ColeccionCanonica:

    def __init__(self, gramatica):
        self.gramatica = aumentar(gramatica)
        self.estados = []        # lista de conjuntos de elementos (I0, I1…)
        self.transiciones = {}   # (i, X) -> j, o ACEPTACION
        self.pasos = []          # registro de la corrida, para la salida

    # ------------------------------------------------------------------
    # ALGORITMOS
    # ------------------------------------------------------------------

    def simbolo_despues_punto(self, elemento):
        p, k = elemento
        derecha = self.gramatica.producciones[p][1]
        return derecha[k] if k < len(derecha) else None

    def cerradura(self, elementos):
        resultado = list(elementos)
        # Recorrer la lista mientras crece equivale al "hacer … mientras
        # haya elementos por añadir": cada elemento nuevo también se revisa.
        i = 0
        while i < len(resultado):
            b = self.simbolo_despues_punto(resultado[i])
            if b is not None and self.gramatica.es_no_terminal(b):
                for p, (izq, _) in enumerate(self.gramatica.producciones):
                    if izq == b and (p, 0) not in resultado:
                        resultado.append((p, 0))
            i += 1
        return resultado

    def nucleo_ir_a(self, estado, x):
        """J = {[A → αX·β] | [A → α·Xβ] en el estado}."""
        return [(p, k + 1) for p, k in estado
                if self.simbolo_despues_punto((p, k)) == x]

    def ir_a(self, estado, x):
        return self.cerradura(self.nucleo_ir_a(estado, x))

    def calcular(self):
        self.estados = [self.cerradura([(0, 0)])]
        self.transiciones = {}
        self.pasos = [("inicio", [(0, 0)])]
        conjuntos = [frozenset(self.estados[0])]

        i = 0
        while i < len(self.estados):   # C crece mientras se recorre
            for x in self.simbolos_transicion(self.estados[i]):
                if x == FIN:
                    self.transiciones[(i, x)] = ACEPTACION
                    self.pasos.append(("aceptacion", i))
                    continue
                nucleo = self.nucleo_ir_a(self.estados[i], x)
                destino = self.cerradura(nucleo)
                clave = frozenset(destino)
                nuevo = clave not in conjuntos
                if nuevo:
                    self.estados.append(destino)
                    conjuntos.append(clave)
                j = conjuntos.index(clave)
                self.transiciones[(i, x)] = j
                self.pasos.append(("ir_a", i, x, nucleo, j, nuevo))
            i += 1
        return self

    def simbolos_transicion(self, estado):
        """Símbolos X con ·X en el estado, en el orden en que aparecen."""
        simbolos = (self.simbolo_despues_punto(e) for e in estado)
        return list(dict.fromkeys(s for s in simbolos if s is not None))

    # ------------------------------------------------------------------
    # SALIDAS
    # ------------------------------------------------------------------

    def formatear_elemento(self, elemento):
        p, k = elemento
        izq, derecha = self.gramatica.producciones[p]
        return (f"[{izq}→{''.join(derecha[:k])}{PUNTO}"
                f"{''.join(derecha[k:])}]")

    def formatear_conjunto(self, elementos):
        return "{" + "".join(self.formatear_elemento(e)
                             for e in elementos) + "}"

    def _linea_estado(self, j, sangria):
        return [(f"{sangria}I{j}={self.formatear_conjunto(self.estados[j])}",
                 "estado")]

    def lineas(self):
        """Colección canónica como en el ejemplo de clase. Cada línea es
        una lista de segmentos (texto, tipo); el tipo sirve para dar color
        en la interfaz."""
        lineas = []
        for paso in self.pasos:
            if paso[0] == "inicio":
                lineas.append([(f"cerradura({self.formatear_conjunto(paso[1])})=",
                                "cerradura")])
                lineas.append(self._linea_estado(0, ""))
            elif paso[0] == "aceptacion":
                lineas.append([(f"cerr(Ir_a(I{paso[1]},{FIN}))={ACEPTACION}",
                                "aceptacion")])
            else:
                _, i, x, nucleo, j, nuevo = paso
                texto = (f"cerr(Ir_a(I{i},{x}))="
                         f"cerr({self.formatear_conjunto(nucleo)})")
                if nuevo:
                    lineas.append([(texto, "ir_a")])
                    lineas.append(self._linea_estado(j, "      "))
                else:
                    lineas.append([(f"{texto} = I{j}", "existente")])
        return lineas

    def reporte(self):
        return "\n".join("".join(texto for texto, _ in linea)
                         for linea in self.lineas())

    def lineas_gramatica(self):
        """Gramática aumentada, una producción por línea."""
        return [f"{izq} → {' '.join(der) if der else EPSILON}"
                for izq, der in self.gramatica.producciones]
