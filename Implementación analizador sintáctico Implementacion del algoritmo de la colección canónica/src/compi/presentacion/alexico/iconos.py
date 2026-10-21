"""Iconos de la interfaz (♡ ✿ 💾 ✓ ✗ ⚠ 📁 📄 ⚙ ▶) dibujados como imágenes.

Cuando Tk no usa Xft (como el Python de uv en Linux) la única fuente que
dibuja → y ε es "fixed", que no trae estos símbolos y los muestra como
cuadritos. En ese caso el símbolo se quita del texto y se pone una imagen
(pixel art de 16×16) al lado; con las demás fuentes se deja el texto tal
cual, con sus símbolos.

Uso:  ttk.Button(padre, command=…, **con_icono("♡  Abrir"))
      etiqueta.config(**con_icono("✓  Listo"))
"""

import math
import tkinter as tk
from tkinter import ttk

from .estilos import COLORES, FUENTES

_PALETA = {
    "R": COLORES["rosa_oscuro"], "P": COLORES["rosa"],
    "L": COLORES["rosa_claro"], "W": COLORES["blanco"],
    "D": COLORES["texto"], "G": "#3E8E5E", "X": "#C62828",
    "Y": "#F2C230", "O": "#C98A1B", "B": "#6B7FA8", "A": "#9AA9C9",
}

_DIBUJOS = {
    "corazon": """
        ................
        ................
        ..RRR.....RRR...
        .RPPPR...RPPPR..
        RPWWPPR.RPPPPPR.
        RPWPPPPRPPPPPPR.
        RPPPPPPPPPPPPPR.
        RPPPPPPPPPPPPPR.
        .RPPPPPPPPPPPR..
        ..RPPPPPPPPPR...
        ...RPPPPPPPR....
        ....RPPPPPR.....
        .....RPPPR......
        ......RPR.......
        .......R........
    """,
    "flor": """
        ......RRR.......
        .....RPPPR......
        .RR..RPPPR..RR..
        RPPR.RPPPR.RPPR.
        RPPPRRPPPRRPPPR.
        .RPPPRRYRRPPPR..
        ..RRRRYOYRRRR...
        .....YOYOY......
        ..RRRRYOYRRRR...
        .RPPPRRYRRPPPR..
        RPPPRRPPPRRPPPR.
        RPPR.RPPPR.RPPR.
        .RR..RPPPR..RR..
        .....RPPPR......
        ......RRR.......
    """,
    "disco": """
        BBBBBBBBBBBBBB..
        BBAWWWWWWWWABBB.
        BBAWWWWWWWWABBBB
        BBAWWWWWWWWABBBB
        BBAWWWWWWWWABBBB
        BBAAAAAAAAAABBBB
        BBBBBBBBBBBBBBBB
        BBBBBBBBBBBBBBBB
        BBBDDDDDDDDDDBBB
        BBBDDWWWWWWDDBBB
        BBBDDWWWWWWDDBBB
        BBBDDWWWWWWDDBBB
        BBBDDDDDDDDDDBBB
        BBBBBBBBBBBBBBBB
    """,
    "palomita": """
        ................
        ..............GG
        .............GGG
        ............GGG.
        ...........GGG..
        ..........GGG...
        .GG......GGG....
        .GGG....GGG.....
        ..GGG..GGG......
        ...GGGGGG.......
        ....GGGG........
        .....GG.........
    """,
    "tache": """
        ................
        ..XX........XX..
        ..XXX......XXX..
        ...XXX....XXX...
        ....XXX..XXX....
        .....XXXXXX.....
        ......XXXX......
        ......XXXX......
        .....XXXXXX.....
        ....XXX..XXX....
        ...XXX....XXX...
        ..XXX......XXX..
        ..XX........XX..
    """,
    "advertencia": """
        .......OO.......
        ......OYYO......
        ......OYYO......
        .....OYYYYO.....
        .....OYDDYO.....
        ....OYYDDYYO....
        ....OYYDDYYO....
        ...OYYYDDYYYO...
        ...OYYYDDYYYO...
        ..OYYYYYYYYYYO..
        ..OYYYYDDYYYYO..
        .OYYYYYDDYYYYYO.
        .OYYYYYYYYYYYYO.
        OOOOOOOOOOOOOOOO
    """,
    "carpeta": """
        ................
        .OOOOO..........
        OYYYYYO.........
        OYYYYYYOOOOOOOO.
        OYYYYYYYYYYYYYO.
        OOOOOOOOOOOOOOOO
        OYYYYYYYYYYYYYYO
        OYYYYYYYYYYYYYYO
        OYYYYYYYYYYYYYYO
        OYYYYYYYYYYYYYYO
        OYYYYYYYYYYYYYYO
        OYYYYYYYYYYYYYYO
        OOOOOOOOOOOOOOOO
    """,
    "documento": """
        ..DDDDDDDD......
        ..DWWWWWWDD.....
        ..DWWWWWWDWD....
        ..DWWWWWWDDDD...
        ..DWWWWWWWWWD...
        ..DWAAAAAAWWD...
        ..DWWWWWWWWWD...
        ..DWAAAAAAAWD...
        ..DWWWWWWWWWD...
        ..DWAAAAAAAWD...
        ..DWWWWWWWWWD...
        ..DWAAAAAWWWD...
        ..DWWWWWWWWWD...
        ..DDDDDDDDDDD...
    """,
    "reproducir": """
        ...RR...........
        ...RPRR.........
        ...RPPPRR.......
        ...RPPPPPRR.....
        ...RPPPPPPPRR...
        ...RPPPPPPPPPR..
        ...RPPPPPPPPPR..
        ...RPPPPPPPRR...
        ...RPPPPPRR.....
        ...RPPPRR.......
        ...RPRR.........
        ...RR...........
    """,
}

# Símbolo del texto -> nombre del icono.
SIMBOLOS = {
    "♡": "corazon", "✿": "flor", "💾": "disco", "✓": "palomita",
    "✗": "tache", "⚠": "advertencia", "📁": "carpeta", "📄": "documento",
    "⚙": "engrane", "▶": "reproducir",
}

_TAMANO = 16
_cache = {}


def usar_imagenes():
    """True si la fuente elegida no puede dibujar los símbolos."""
    return FUENTES["ui"] == "fixed"


def icono(nombre, escala=1):
    """PhotoImage del icono (se guarda en caché para que Tk no la pierda)."""
    clave = (nombre, escala)
    if clave not in _cache:
        imagen = _dibujar(nombre)
        _cache[clave] = imagen.zoom(escala) if escala > 1 else imagen
    return _cache[clave]


def con_icono(texto):
    """Opciones text/image/compound para un Label o Button.

    Un símbolo al inicio ("♡  Abrir") queda a la izquierda y uno al final
    ("Guardado ✓") a la derecha. Si no hay símbolo, se quita la imagen que
    tuviera el widget.
    """
    if not usar_imagenes():
        return {"text": texto}
    limpio = texto.strip()
    for simbolo, nombre in SIMBOLOS.items():
        if limpio.startswith(simbolo):
            return {"text": " " + limpio[len(simbolo):].strip(),
                    "image": icono(nombre), "compound": "left"}
        if limpio.endswith(simbolo):
            return {"text": limpio[:-len(simbolo)].strip() + " ",
                    "image": icono(nombre), "compound": "right"}
    return {"text": texto, "image": ""}


def crear_titulo(padre, texto):
    """Título "✿  TEXTO  ✿": con imágenes, una flor a cada lado."""
    if not usar_imagenes():
        return ttk.Label(padre, text=texto, style="Titulo.TLabel")
    marco = ttk.Frame(padre)
    limpio = texto.strip()
    simbolo = next((s for s in SIMBOLOS if limpio.startswith(s)), None)
    if simbolo is None:
        ttk.Label(marco, text=texto, style="Titulo.TLabel").pack()
        return marco
    nombre = SIMBOLOS[simbolo]
    limpio = limpio.strip(simbolo).strip()
    ttk.Label(marco, image=icono(nombre, 2)).pack(side="left")
    ttk.Label(marco, text=f"  {limpio}  ", style="Titulo.TLabel").pack(
        side="left")
    ttk.Label(marco, image=icono(nombre, 2)).pack(side="left")
    return marco


# ----------------------------------------------------------------------

def _dibujar(nombre):
    if nombre == "engrane":
        filas = _engrane()
    else:
        filas = [f.strip() for f in _DIBUJOS[nombre].strip().splitlines()]
    # Centrar verticalmente en 16×16.
    arriba = (_TAMANO - len(filas)) // 2
    filas = (["." * _TAMANO] * arriba + filas
             + ["." * _TAMANO] * (_TAMANO - arriba - len(filas)))

    imagen = tk.PhotoImage(width=_TAMANO, height=_TAMANO)
    for y, fila in enumerate(filas):
        for x, c in enumerate(fila.ljust(_TAMANO, ".")[:_TAMANO]):
            if c in _PALETA:
                imagen.put(_PALETA[c], (x, y))
    return imagen


def _engrane():
    """Engrane calculado: anillo con 8 dientes y un hueco al centro."""
    filas = []
    for y in range(_TAMANO):
        fila = ""
        for x in range(_TAMANO):
            dx, dy = x - 7.5, y - 7.5
            r = math.hypot(dx, dy)
            diente = math.cos(8 * math.atan2(dy, dx)) > 0.2
            if r < 2.3:
                fila += "."
            elif r < 5.3 or (r < 7.6 and diente):
                fila += "A" if r < 3.4 else "B"
            else:
                fila += "."
        filas.append(fila)
    return filas
