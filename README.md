# Compilador C++ → Java

Proyecto del curso de **Compiladores** (Instituto de Computación, Universidad
Tecnológica de la Mixteca).

Es un compilador que toma programas escritos en **C++** (lenguaje fuente) y los
traducirá a **Java** (lenguaje destino). Está escrito en **Python** con interfaz
gráfica en **Tkinter**.

> **Proyecto en proceso.** El compilador se construye por fases, una
> asignación a la vez. Cada carpeta de este repositorio es una asignación
> entregada; las siguientes se irán agregando conforme se terminen.

---

## Avance

| Fase | Asignación | Estado | Carpeta |
|------|------------|--------|---------|
| Análisis léxico | Asignación 1 — Implementación de analizador lexico usando un AFD | Terminada | [`Implementación de analizador lexico usando un AFD/`](<Implementación de analizador lexico usando un AFD/>) |
| Análisis léxico | Asignación 2 — Analizador léxico en Flex | Por subir | — |
| Análisis sintáctico | Asignación 3 — Primeros y Siguientes | Por subir | — |
| Análisis sintáctico | Asignación 4 — Colección canónica | Por subir | — |
| Análisis semántico | — | Pendiente | — |
| Generación de código Java | — | Pendiente | — |

---

## Estructura del repositorio

```
Compilador-Cpp-a-Java/
├── README.md                        Este archivo: qué es el proyecto y su avance
├── .gitignore                       Archivos que Git no debe subir
└── Implementación de analizador lexico usando un AFD/
    │                                Asignación 1: analizador léxico basado en un AFD
    ├── src/                         Código de la interfaz y del analizador
    ├── archivos_prueba/             Programas C++ de ejemplo
    ├── automata/                    Diseño del AFD (JFLAP e imagen)
    ├── documentacion/               Enunciado, expresiones regulares, UML, bitácoras
    ├── ejecutable/                  AnalizadorLexico.exe para Windows
    ├── capturas/                    Imágenes de la interfaz
    └── iniciar.bat / .sh / .command Lanzadores para cada sistema
```

Cada asignación tiene su propio `README.md`, que explica qué hace, el contenido
de cada carpeta y cómo ejecutarla.

---

## Vista rápida

![Implementación de analizador lexico usando un AFD](<Implementación de analizador lexico usando un AFD/capturas/ventana_principal.png>)

---

## Cómo probarlo

- **Windows, sin instalar nada:** descarga el `.exe` de la carpeta `ejecutable/`
  de la asignación y ábrelo con doble clic.
- **Cualquier sistema, desde el código:** instala Python 3.9 o superior con
  Tkinter y ejecuta el lanzador de la asignación (`iniciar.bat`, `iniciar.sh` o
  `iniciar.command`).

Los detalles están en el README de cada asignación.
