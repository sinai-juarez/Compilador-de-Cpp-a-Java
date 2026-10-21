"""Controles tabulares reutilizables."""

from tkinter import ttk


def crear_tabla(padre, columnas, encabezados, anchos, solo_vertical=False):
    marco = ttk.Frame(padre)
    tabla = ttk.Treeview(marco, columns=columnas, show="headings")
    for columna, encabezado, ancho in zip(columnas, encabezados, anchos):
        tabla.heading(columna, text=encabezado)
        tabla.column(columna, width=ancho, anchor="w")

    scroll_y = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll_y.set)
    tabla.grid(row=0, column=0, sticky="nsew", padx=(4, 0), pady=4)
    scroll_y.grid(row=0, column=1, sticky="ns", pady=4)

    if not solo_vertical:
        scroll_x = ttk.Scrollbar(marco, orient="horizontal",
                                 command=tabla.xview)
        tabla.configure(xscrollcommand=scroll_x.set)
        scroll_x.grid(row=1, column=0, sticky="ew", padx=(4, 0))

    marco.rowconfigure(0, weight=1)
    marco.columnconfigure(0, weight=1)
    return marco, tabla
