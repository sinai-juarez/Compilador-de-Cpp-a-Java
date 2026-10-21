# Compilador C++ → Java

Proyecto del curso de **Compiladores**, de quinto semestre de la carrera de
**Ingeniería en Computación**, Universidad Tecnológica de la Mixteca.

Es un compilador que toma programas escritos en **C++** (lenguaje fuente) y los
traducirá a **Java** (lenguaje destino). Está escrito en **Python** con interfaz
gráfica en **Tkinter**; a partir de la Asignación 2 el analizador léxico también
se genera con **Flex**.

> **Proyecto en proceso.** El compilador se construye por fases, una
> asignación a la vez. Cada carpeta de este repositorio es una asignación
> entregada; las siguientes se irán agregando conforme se terminen.

---

## Avance

| Fase | Asignación | Estado | Carpeta |
|------|------------|--------|---------|
| Análisis léxico | Asignación 1 — Implementación de analizador lexico usando un AFD | Terminada | [`Implementación de analizador lexico usando un AFD/`](<Implementación de analizador lexico usando un AFD/>) |
| Análisis léxico | Asignación 2 — Implementación del analizador léxico en Flex | Terminada | [`Implementación del analizador léxico en Flex/`](<Implementación del analizador léxico en Flex/>) |
| Análisis sintáctico | Asignación 3 — Implementación del algoritmo Primeros y Siguientes | Terminada | [`Analizador sintáctico Implementación del algoritmo primeros y siguientes/`](<Analizador sintáctico Implementación del algoritmo primeros y siguientes/>) |
| Análisis sintáctico | Asignación 4 — Implementación del algoritmo de la colección canónica | Terminada | [`Implementación analizador sintáctico Implementacion del algoritmo de la colección canónica/`](<Implementación analizador sintáctico Implementacion del algoritmo de la colección canónica/>) |
| Análisis semántico | — | Pendiente | — |
| Generación de código Java | — | Pendiente | — |

---

## Estructura del repositorio

```
Compilador-Cpp-a-Java/
├── README.md                        Este archivo: qué es el proyecto y su avance
├── .gitignore                       Archivos que Git no debe subir
├── Implementación de analizador lexico usando un AFD/
│   │                                Asignación 1: analizador léxico basado en un AFD
│   ├── src/                         Código de la interfaz y del analizador
│   ├── archivos_prueba/             Programas C++ de ejemplo
│   ├── automata/                    Diseño del AFD (JFLAP e imagen)
│   ├── documentacion/               Enunciado, expresiones regulares, UML, bitácoras
│   ├── ejecutable/                  AnalizadorLexico.exe para Windows
│   ├── capturas/                    Imágenes de la interfaz
│   └── iniciar.bat / .sh / .command Lanzadores para cada sistema
├── Implementación del analizador léxico en Flex/
│   │                                Asignación 2: analizador léxico generado con Flex
│   ├── flex/                        lexer.l (especificación en Flex)
│   ├── src/                         Interfaz por capas (persistencia y presentación)
│   ├── archivos_prueba/             Programas C++ de ejemplo
│   ├── documentacion/               Informe, asignación de actividades y bitácora
│   ├── ejecutable/                  AnalizadorLexicoFlex.exe para Windows
│   ├── herramientas/                win_flex y TinyCC que usa el .exe de Windows
│   ├── imagenes/                    Logo de la pantalla de inicio
│   ├── capturas/                    Imágenes de la interfaz
│   └── iniciar.bat / .sh / .command Lanzadores para cada sistema
├── Analizador sintáctico Implementación del algoritmo primeros y siguientes/
│   │                                Asignación 3: conjuntos PRIMERO y SIGUIENTE de una gramática
│   ├── gramaticas/                  Gramáticas 1 a 6 de la asignación
│   ├── src/                         Interfaz por capas, con el analizador sintáctico agregado
│   ├── archivos_prueba/             Programas C++ de ejemplo
│   ├── documentacion/               Informe, asignación de actividades y bitácora
│   ├── ejecutable/                  PrimerosSiguientes.exe para Windows
│   ├── flex/, herramientas/         Analizador léxico en Flex de la Asignación 2
│   ├── imagenes/                    Logo de la pantalla de inicio
│   ├── capturas/                    Imágenes de la interfaz
│   └── iniciar.bat / .sh / .command Lanzadores para cada sistema
└── Implementación analizador sintáctico Implementacion del algoritmo de la colección canónica/
    │                                Asignación 4: colección canónica de elementos LR(0)
    ├── gramaticasAumentadas/        Gramáticas 1 a 6 aumentadas (S' → S $)
    ├── gramaticas/                  Gramáticas 1 a 6 sin aumentar
    ├── src/                         Interfaz por capas, con la colección canónica agregada
    ├── archivos_prueba/             Programas C++ de ejemplo
    ├── documentacion/               Informe, asignación de actividades y bitácora
    ├── flex/, herramientas/         Analizador léxico en Flex de la Asignación 2
    ├── imagenes/                    Logo de la pantalla de inicio
    ├── capturas/                    Imágenes de la interfaz
    └── iniciar.bat / .sh / .command Lanzadores para cada sistema
```

Cada asignación tiene su propio `README.md`, que explica qué hace, el contenido
de cada carpeta y cómo ejecutarla.

---

## Vista rápida

| Asignación 1 — AFD | Asignación 2 — Flex |
|:-:|:-:|
| ![Analizador léxico con AFD](<Implementación de analizador lexico usando un AFD/capturas/ventana_principal.png>) | ![Analizador léxico en Flex](<Implementación del analizador léxico en Flex/capturas/ventana_principal.png>) |

| Asignación 3 — Primeros y Siguientes | Asignación 4 — Colección canónica |
|:-:|:-:|
| ![Cálculo de primeros y siguientes](<Analizador sintáctico Implementación del algoritmo primeros y siguientes/capturas/primeros_siguientes.png>) | ![Cálculo de la colección canónica](<Implementación analizador sintáctico Implementacion del algoritmo de la colección canónica/capturas/coleccion_canonica.png>) |

---

## Cómo probarlo

- **Windows, sin instalar nada:** descarga el `.exe` de la carpeta `ejecutable/`
  de la asignación y ábrelo con doble clic (Asignaciones 1 a 3; la Asignación 4
  explica en su README cómo generarlo).
- **Cualquier sistema, desde el código:** instala Python 3.9 o superior con
  Tkinter y ejecuta el lanzador de la asignación (`iniciar.bat`, `iniciar.sh` o
  `iniciar.command`). El analizador en Flex (Asignaciones 2 a 4)
  necesita además `flex` y `gcc` en Linux y macOS.

Los detalles están en el README de cada asignación.
