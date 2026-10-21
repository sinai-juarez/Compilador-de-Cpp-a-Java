"""Editor del programa fuente con numeración de líneas."""

import tkinter as tk
from tkinter import ttk

from .estilos import COLORES, FUENTES


class EditorCodigo(ttk.LabelFrame):
    """Área de texto con una columna de números de línea sincronizada.

    `al_modificar` se invoca sin argumentos cada vez que cambia el contenido.
    """

    def __init__(self, padre, al_modificar=None):
        super().__init__(padre, text="  Código fuente  ")
        self.al_modificar = al_modificar
        self._total_lineas = 0
        fuente = (FUENTES["codigo"], 11)

        self.numeros = tk.Text(
            self, width=4, wrap="none", state="disabled", font=fuente,
            bg=COLORES["rosa_claro"], fg=COLORES["rosa_oscuro"],
            relief="flat", bd=0, highlightthickness=0,
            padx=6, pady=8, takefocus=0, cursor="arrow")
        self.numeros.tag_configure("derecha", justify="right")
        # Sin los bindings de Text la columna no se puede seleccionar ni
        # recibe foco; la rueda del ratón se reenvía al código.
        self.numeros.bindtags((str(self.numeros), str(self), "all"))
        for evento in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.numeros.bind(evento, self._rueda_sobre_numeros)

        self.texto = tk.Text(
            self, wrap="none", undo=True, font=fuente,
            bg=COLORES["blanco"], fg=COLORES["texto"],
            insertbackground=COLORES["rosa_oscuro"],
            selectbackground=COLORES["rosa_claro"],
            selectforeground=COLORES["texto"], relief="flat", bd=0,
            highlightthickness=0, padx=10, pady=8)

        self.scroll_y = ttk.Scrollbar(self, orient="vertical",
                                      command=self.texto.yview)
        scroll_x = ttk.Scrollbar(self, orient="horizontal",
                                 command=self.texto.xview)
        self.texto.configure(yscrollcommand=self._al_desplazar,
                             xscrollcommand=scroll_x.set)

        self.numeros.grid(row=0, column=0, sticky="ns", padx=(5, 0), pady=5)
        self.texto.grid(row=0, column=1, sticky="nsew", pady=5)
        self.scroll_y.grid(row=0, column=2, sticky="ns", pady=5)
        scroll_x.grid(row=1, column=1, sticky="ew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.texto.bind("<<Modified>>", self._modificado)
        self._actualizar_numeros()

    def contenido(self):
        return self.texto.get("1.0", "end-1c")

    def cargar(self, contenido):
        self.limpiar()
        self.texto.insert("1.0", contenido)

    def limpiar(self):
        self.texto.delete("1.0", tk.END)

    def _modificado(self, _evento=None):
        try:
            self.texto.edit_modified(False)
        except tk.TclError:
            pass
        self._actualizar_numeros()
        if self.al_modificar:
            self.al_modificar()

    def _actualizar_numeros(self):
        total = int(self.texto.index("end-1c").split(".")[0])
        if total == self._total_lineas:
            return
        self._total_lineas = total

        self.numeros.configure(state="normal",
                               width=max(3, len(str(total))) + 1)
        self.numeros.delete("1.0", tk.END)
        self.numeros.insert(
            "1.0", "\n".join(str(n) for n in range(1, total + 1)), "derecha")
        self.numeros.configure(state="disabled")
        self.numeros.yview_moveto(self.texto.yview()[0])

    def _al_desplazar(self, primero, ultimo):
        self.scroll_y.set(primero, ultimo)
        self.numeros.yview_moveto(primero)

    def _rueda_sobre_numeros(self, evento):
        if evento.num == 4:
            pasos = -1
        elif evento.num == 5:
            pasos = 1
        else:
            pasos = -1 if evento.delta > 0 else 1
        self.texto.yview_scroll(pasos * 3, "units")
        return "break"
