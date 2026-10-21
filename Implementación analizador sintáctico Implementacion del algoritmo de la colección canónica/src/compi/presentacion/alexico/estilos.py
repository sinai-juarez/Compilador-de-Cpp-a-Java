"""Paleta y estilos compartidos por los componentes de la interfaz."""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


COLORES = {
    "rosa_oscuro": "#B94F7B",
    "rosa": "#E98FB3",
    "rosa_claro": "#FCE4EF",
    "rosa_muy_claro": "#FFF7FB",
    "rosa_borde": "#E5B0C7",
    "fondo": "#FFF9FC",
    "texto": "#593B49",
    "blanco": "#FFFFFF",
}

# Primera familia instalada de cada lista; si no hay ninguna, la de Tk.
# "fixed" va al final: cuando Tk no usa Xft (como el Python de uv en
# Linux) solo ve las fuentes de X11, y con courier/helvetica la → y la ε se
# dibujan como "®" y "e∝"; la fuente "fixed" sí trae esos caracteres.
_FAMILIAS_UI = ("DejaVu Sans", "Segoe UI", "Helvetica Neue", "Arial", "fixed")
_FAMILIAS_CODIGO = ("DejaVu Sans Mono", "Consolas", "Menlo", "Courier New",
                    "fixed")
# Fuentes con nombre de Tk que usan los widgets sin fuente propia
# (cuadros de mensaje, menús, entradas).
_FUENTES_TK = ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont",
               "TkCaptionFont", "TkSmallCaptionFont", "TkTooltipFont")

# Se completa en configurar_estilos, cuando ya existe la ventana raíz.
FUENTES = {"ui": "TkDefaultFont", "codigo": "TkFixedFont"}


def _elegir_familia(ventana, candidatas, fuente_tk):
    instaladas = set(tkfont.families(ventana))
    respaldo = tkfont.nametofont(fuente_tk).actual("family")
    return next((f for f in candidatas if f in instaladas), respaldo)


def configurar_estilos(ventana):
    FUENTES["ui"] = _elegir_familia(ventana, _FAMILIAS_UI, "TkDefaultFont")
    FUENTES["codigo"] = _elegir_familia(ventana, _FAMILIAS_CODIGO, "TkFixedFont")
    ui = FUENTES["ui"]
    if ui == "fixed":
        for nombre in _FUENTES_TK:
            tkfont.nametofont(nombre, ventana).configure(family=ui)
        tkfont.nametofont("TkFixedFont", ventana).configure(family=ui)

    estilo = ttk.Style(ventana)
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass
    estilo.configure("TFrame", background=COLORES["fondo"])
    estilo.configure("TLabel", background=COLORES["fondo"],
                     foreground=COLORES["texto"], font=(ui, 10))
    estilo.configure("Titulo.TLabel", background=COLORES["fondo"],
                     foreground=COLORES["rosa_oscuro"],
                     font=(ui, 19, "bold"))
    estilo.configure("TLabelframe", background=COLORES["fondo"],
                     bordercolor=COLORES["rosa_borde"], relief="solid")
    estilo.configure("TLabelframe.Label", background=COLORES["fondo"],
                     foreground=COLORES["rosa_oscuro"],
                     font=(ui, 10, "bold"))
    estilo.configure("TButton", background=COLORES["rosa_claro"],
                     foreground=COLORES["texto"],
                     bordercolor=COLORES["rosa_borde"],
                     font=(ui, 10, "bold"), padding=(13, 7))
    estilo.map("TButton", background=[("active", COLORES["rosa"]),
                                      ("disabled", "#F2E7ED")],
               foreground=[("disabled", "#AA9BA2")])
    estilo.configure("TNotebook", background=COLORES["fondo"],
                     bordercolor=COLORES["rosa_borde"])
    estilo.configure("TNotebook.Tab", background=COLORES["rosa_claro"],
                     foreground=COLORES["texto"], padding=(16, 8),
                     font=(ui, 10, "bold"))
    estilo.map("TNotebook.Tab", background=[("selected", COLORES["rosa"])],
               foreground=[("selected", COLORES["blanco"])])
    estilo.configure("Treeview", background=COLORES["blanco"],
                     foreground=COLORES["texto"],
                     fieldbackground=COLORES["blanco"],
                     rowheight=25, font=(ui, 10))
    estilo.configure("Treeview.Heading", background=COLORES["rosa_claro"],
                     foreground=COLORES["rosa_oscuro"],
                     font=(ui, 10, "bold"))
    estilo.map("Treeview", background=[("selected", COLORES["rosa_claro"])],
               foreground=[("selected", COLORES["texto"])])
