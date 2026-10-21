from compi.persistencia.analizadorLexico.generales.tokens import ErrorLexico, TokenLexico

# ============================================================
# ANALIZADOR LÉXICO
# ============================================================

class AnalizadorLexico:

    def __init__(
        self,
        fuente: str,
        afd
    ):

        self.fuente = fuente

        self.posicion = 0

        self.linea = 1

        self.columna = 1

        self.afd = afd

        self.errores = []
        self.comentarios = []

    # ========================================================
    # ANALIZAR
    # ========================================================

    def analizar(self) -> list[TokenLexico]:

        tokens = []

        while self.posicion < len(self.fuente):

            self.omitir_espacios()

            if self.posicion >= len(self.fuente):
                break

            token = self.siguiente_token()

            if token is not None:

            # ----------------------------------------------
            # LOS COMENTARIOS NO SE AGREGAN A TOKENS
            # ----------------------------------------------

                if token.token == "comLinea":
                 self.comentarios.append(token)

                elif token.token == "comBloque":
                    self.comentarios.append(token)

                else:
                    tokens.append(token)

        return tokens
    # ========================================================
    # SIGUIENTE TOKEN
    # ========================================================

    def siguiente_token(self):

        linea_inicio = self.linea
        columna_inicio = self.columna
        inicio = self.posicion

        estado = self.afd.estadoInicial

        ultimo_estado_final = None
        ultima_posicion_final = inicio

        # --------------------------------------------------------
        # ¿ESTAMOS INTENTANDO LEER UNA CADENA?
        # --------------------------------------------------------

        es_string = (
            self.posicion < len(self.fuente)
            and self.fuente[self.posicion] == '"'
        )

        # --------------------------------------------------------
        # ¿ESTAMOS INTENTANDO LEER UN CARÁCTER?
        # --------------------------------------------------------

        es_caracter = (
            self.posicion < len(self.fuente)
            and self.fuente[self.posicion] == "'"
        )
        #--------------------------------------------------------
        # ¿ESTAMOS INTENTANDO LEER UN COMENTARIO DE BLOQUE?
        # --------------------------------------------------------

        es_comentario_bloque = (
            self.fuente.startswith(
                "/*",
                self.posicion
            )
        )

        # --------------------------------------------------------
        # COMENTARIO DE BLOQUE SIN CERRAR
        # Se revisa antes de recorrer el AFD: "/" ya es un estado
        # final, así que el AFD devolvería "/" como token válido y el
        # resto del comentario se leería como código.
        # Recuperación: se descarta el resto del archivo.
        # --------------------------------------------------------

        if (
            es_comentario_bloque
            and self.fuente.find("*/", self.posicion + 2) == -1
        ):

            self.errores.append(ErrorLexico(
                linea_inicio,
                columna_inicio,
                "/*",
                "Comentario de bloque sin cerrar"
            ))

            self.posicion = len(self.fuente)

            return None

        # ========================================================
        # RECORRER EL LEXEMA
        # ========================================================

        while self.posicion < len(self.fuente):

            caracter = self.fuente[self.posicion]

            nuevo_estado = self.afd.transitar(
                estado,
                caracter
            )

            # ----------------------------------------------------
            # NO EXISTE TRANSICIÓN
            # ----------------------------------------------------

            if nuevo_estado is None:
                break

            estado = nuevo_estado
            self.posicion += 1

            # ----------------------------------------------------
            # GUARDAR ÚLTIMO ESTADO FINAL
            # ----------------------------------------------------

            if self.afd.esFinal(estado):

                ultimo_estado_final = estado
                ultima_posicion_final = self.posicion
        # ========================================================
        # TOKEN VÁLIDO
        # ========================================================

        if ultimo_estado_final is not None:

            lexema = self.fuente[
                inicio:ultima_posicion_final
            ]

            # ----------------------------------------------------
            # REGRESAR A LA ÚLTIMA POSICIÓN FINAL
            # ----------------------------------------------------
            self.posicion = ultima_posicion_final
            # ----------------------------------------------------
            # ACTUALIZAR LÍNEA Y COLUMNA
            # ----------------------------------------------------

            self.linea = linea_inicio
            self.columna = columna_inicio

            for caracter in lexema:

                if caracter == "\n":

                    self.linea += 1
                    self.columna = 1

                else:

                    self.columna += 1

            # ----------------------------------------------------
            # RECONOCER TIPO DE TOKEN
            # ----------------------------------------------------

            tipo_token = self.afd.reconocer(
                lexema
            )

            return TokenLexico(
                linea_inicio,
                columna_inicio,
                tipo_token,
                lexema,
                lexema
            )
        # ========================================================
        # AQUÍ TENEMOS UN ERROR LÉXICO
        # ========================================================
        # --------------------------------------------------------
        # CASO 1: STRING SIN CERRAR
        # --------------------------------------------------------
        if es_string:

            error = ErrorLexico(
                linea_inicio,
                columna_inicio,
                '"',
                "Cadena sin cerrar"
            )

            self.errores.append(error)

            # ----------------------------------------------------
            # RECUPERACIÓN:
            # Avanzamos hasta el salto de línea.
            # NO nos vamos hasta el final del archivo.
            # ----------------------------------------------------

            while (
                self.posicion < len(self.fuente)
                and self.fuente[self.posicion]
                not in "\r\n"
            ):

                self.posicion += 1

            # ----------------------------------------------------
            # Dejamos que omitir_espacios() procese el Enter
            # ----------------------------------------------------

            self.linea = linea_inicio + 1
            self.columna = 1

            if self.posicion < len(self.fuente):

                if self.fuente[self.posicion] == "\r":

                    self.posicion += 1

                    if (
                        self.posicion < len(self.fuente)
                        and self.fuente[self.posicion] == "\n"
                    ):

                        self.posicion += 1

                elif self.fuente[self.posicion] == "\n":

                    self.posicion += 1

            return None

        # --------------------------------------------------------
        # CASO 2: CARÁCTER SIN CERRAR
        # --------------------------------------------------------

        if es_caracter:

            error = ErrorLexico(
                linea_inicio,
                columna_inicio,
                "'",
                "Caracter sin cerrar"
            )

            self.errores.append(error)

            # ----------------------------------------------------
            # Recuperar hasta Enter
            # ----------------------------------------------------

            while (
                self.posicion < len(self.fuente)
                and self.fuente[self.posicion]
                not in "\r\n"
            ):

                self.posicion += 1

            self.linea = linea_inicio + 1
            self.columna = 1

            if self.posicion < len(self.fuente):

                if self.fuente[self.posicion] == "\r":

                    self.posicion += 1

                    if (
                        self.posicion < len(self.fuente)
                        and self.fuente[self.posicion] == "\n"
                    ):

                        self.posicion += 1

                elif self.fuente[self.posicion] == "\n":

                    self.posicion += 1

            return None


        # ========================================================
        # ERROR NORMAL
        # ========================================================

        if self.posicion < len(self.fuente):

            caracter_error = self.fuente[
                self.posicion
            ]

            error = ErrorLexico(
                linea_inicio,
                columna_inicio,
                caracter_error,
                "Caracter no reconocido"
            )

            self.errores.append(error)

            # ----------------------------------------------------
            # Avanzar un carácter y continuar
            # ----------------------------------------------------

            self.avanzar()

        return None
    # ========================================================
    # AVANZAR
    # ========================================================

    def avanzar(self):

        if self.posicion >= len(self.fuente):

            return

        caracter = self.fuente[
            self.posicion
        ]

        self.posicion += 1

        if caracter == "\n":

            self.linea += 1

            self.columna = 1

        else:

            self.columna += 1
    # ========================================================
    # OMITIR ESPACIOS
    # ========================================================

    def omitir_espacios(self):

        while self.posicion < len(self.fuente):

            caracter = self.fuente[
                self.posicion
            ]


            if caracter in " \t\r\n":

                self.avanzar()

            else:

                break
