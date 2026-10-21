from compi.persistencia.analizadorLexico.generales.tokens import PALABRAS_RESERVADAS, categoria_palabra_reservada

# ============================================================
# ESTADOS FINALES
# ============================================================

class EstadosFinales:

    def __init__(
        self,
        edoFinal: int,
        aceptacion: str
    ):
        self.edoFinal = edoFinal
        self.aceptacion = aceptacion

    def esAceptacion(self) -> bool:
        return True

# ============================================================
# TRANSICIÓN
# ============================================================

class Transicion:

    def __init__(
        self,
        estadoOrigen: int,
        simbolo: str,
        estadoDestino: int
    ):
        self.estadoOrigen = estadoOrigen
        self.simbolo = simbolo
        self.estadoDestino = estadoDestino

    def aplica(self, simbolo: str) -> bool:

        # ----------------------------------------------------
        # LETRA PARA EL PRIMER CARÁCTER DE UN ID
        # ----------------------------------------------------
        if self.simbolo == "LETRA":
            return simbolo.isalpha()

        # ----------------------------------------------------
        # LETRA PARA EL RESTO DEL IDENTIFICADOR
        # Permite letras y _
        # ----------------------------------------------------
        if self.simbolo == "LETRA_ID":
            return simbolo.isalpha() or simbolo == "_"

        # ----------------------------------------------------
        # DÍGITO
        # ----------------------------------------------------
        if self.simbolo == "DIGITO":
            return simbolo.isdigit()

        # ----------------------------------------------------
        # ESPACIO
        # ----------------------------------------------------
        if self.simbolo == "ESPACIO":
            return simbolo in " \t\r\n"

        # ----------------------------------------------------
        # CARACTERES DENTRO DE UN STRING
        # (letra | digito | caracterCadena); la diagonal invertida NO
        # entra aqui: abre una secuencia de escape (ver estado 65 en
        # construir_afd), igual que en la especificacion y el AFD.
        # ----------------------------------------------------
        if self.simbolo == "CARACTER_STRING":
            return simbolo not in '"\\\r\n'
        # ----------------------------------------------------
        # CARÁCTER DENTRO DE COMILLA SIMPLE
        # ----------------------------------------------------
        if self.simbolo == "CARACTER_SIMPLE":
            return simbolo != "'" and simbolo not in "\r\n"

        # ----------------------------------------------------
        # CARACTERES DE COMENTARIO DE LÍNEA
        # No permite Enter porque ahí termina el comentario
        # ----------------------------------------------------
        if self.simbolo == "CARACTER_LINEA":
            return simbolo not in "\r\n"

        # ----------------------------------------------------
        # CARACTERES DE COMENTARIO DE BLOQUE
        # ----------------------------------------------------
        if self.simbolo == "CARACTER_COMENTARIO":
            return True

        # ----------------------------------------------------
        # TRANSICIÓN LITERAL
        # ----------------------------------------------------
        return self.simbolo == simbolo

# ============================================================
# AFD LÉXICO
# ============================================================

class AFDAlexico:

    def __init__(self):

        # Estado inicial
        self.estadoInicial = 0

        # Estado actual
        self.estadoActual = self.estadoInicial

        # Estados finales
        self.estadosFinales = {}

        # Transiciones
        self.transiciones = []

        # Construir AFD
        self.construir_afd()

    # ========================================================
    # AGREGAR ESTADO FINAL
    # ========================================================

    def agregar_estado_final(
        self,
        estado: int,
        aceptacion: str
    ):

        self.estadosFinales[estado] = EstadosFinales(
            estado,
            aceptacion
        )

    # ========================================================
    # AGREGAR TRANSICIÓN
    # ========================================================

    def agregar_transicion(
        self,
        origen: int,
        simbolo: str,
        destino: int
    ):

        self.transiciones.append(
            Transicion(
                origen,
                simbolo,
                destino
            )
        )


    # ========================================================
    # CONSTRUIR AFD
    # ========================================================

    def construir_afd(self):

        # ====================================================
        # DELIMITADORES
        # ====================================================

        self.agregar_transicion(0, "{", 1)
        self.agregar_estado_final(1, "{")
        self.agregar_transicion(0, "}", 2)
        self.agregar_estado_final(2, "}")

        self.agregar_transicion(0, "(", 3)
        self.agregar_estado_final(3, "(")
        self.agregar_transicion(0, ")", 4)
        self.agregar_estado_final(4, ")")

        self.agregar_transicion(0, "[", 5)
        self.agregar_estado_final(5, "[")
        self.agregar_transicion(0, "]", 6)
        self.agregar_estado_final(6, "]")


        # ====================================================
        # DOS PUNTOS Y OPERADOR DE ÁMBITO
        # ====================================================
        self.agregar_transicion(0, ":", 7)
        self.agregar_transicion(7, ":", 8)
        self.agregar_estado_final(7, ":")
        self.agregar_estado_final(8, "::")
        # ====================================================
        # PUNTO
        # ====================================================
        self.agregar_transicion(0, ".", 12)
        self.agregar_estado_final(12, ".")
        # ====================================================
        # PUNTO Y COMA
        # ====================================================
        self.agregar_transicion(0, ";", 13)
        self.agregar_estado_final(13, ";")
        # ====================================================
        # COMA
        # ====================================================
        self.agregar_transicion(0, ",", 10)
        self.agregar_estado_final(10, ",")
        # ====================================================
        # STRINGS
        # ====================================================
        self.agregar_transicion(0, '"', 9)
        self.agregar_transicion( 9, "CARACTER_STRING",9)
        # Secuencia de escape: \( " | \ | n | t | r | ' | 0 ), tal como la
        # define la especificacion y el AFD (estado 9 --\--> 65, y desde 65
        # solo esos 7 caracteres regresan a 9; cualquier otro caracter tras
        # la diagonal invertida es un error lexico, ej. "\z").
        self.agregar_transicion(9, "\\", 65)
        self.agregar_transicion(65, '"', 9)
        self.agregar_transicion(65, "\\", 9)
        self.agregar_transicion(65, "n", 9)
        self.agregar_transicion(65, "t", 9)
        self.agregar_transicion(65, "r", 9)
        self.agregar_transicion(65, "'", 9)
        self.agregar_transicion(65, "0", 9)
        self.agregar_transicion(9,'"',11 )
        self.agregar_estado_final(11,"STRING")

        # ====================================================
        # CARACTERES
        # ====================================================

        self.agregar_transicion(0, "'", 14)
        self.agregar_transicion( 14,"CARACTER_SIMPLE", 15 )
        self.agregar_transicion(15,"'",16)
        self.agregar_estado_final(16,"CARACTER")

        # ====================================================
        # IDENTIFICADORES
        # ====================================================

        self.agregar_transicion(0, "LETRA", 35) 
        self.agregar_transicion(35, "LETRA_ID", 35) 
        self.agregar_transicion(35, "DIGITO", 35)
        self.agregar_estado_final(35, "IDENTIFICADOR")

        # ====================================================
        # ENTEROS
        # ====================================================

        self.agregar_transicion(0, "DIGITO", 32)
        self.agregar_transicion(32, "DIGITO", 32)
        self.agregar_estado_final(32, "NINT")

        # ====================================================
        # FLOTANTES
        # ====================================================
        self.agregar_transicion(32, ".", 33)
        self.agregar_transicion(33, "DIGITO", 34)
        self.agregar_transicion(34, "DIGITO", 34)
        self.agregar_estado_final(34, "NFLOAT")

        # ====================================================
        # SUMA
        # ====================================================

        self.agregar_transicion(0, "+", 54)
        self.agregar_transicion(54, "=", 55)
        self.agregar_transicion(54, "+", 56)

        self.agregar_estado_final(54, "+")
        self.agregar_estado_final(55, "+=")
        self.agregar_estado_final(56, "++")

        # ====================================================
        # RESTA
        # ====================================================

        self.agregar_transicion(0, "-", 50)
        self.agregar_transicion(50, "-", 53)
        self.agregar_transicion(50, "=", 52)
        self.agregar_transicion(50, ">", 51)

        self.agregar_estado_final(50, "-")
        self.agregar_estado_final(53, "--")
        self.agregar_estado_final(52, "-=")
        self.agregar_estado_final(51, "->")

        # ====================================================
        # MULTIPLICACIÓN
        # ====================================================

        self.agregar_transicion(0, "*", 18)
        self.agregar_transicion(18, "=", 19)

        self.agregar_transicion(18, "*", 20)

        self.agregar_estado_final(18, "*")
        self.agregar_estado_final(19, "*=")
        # "**": doble apuntador de C++ (ej. "int **ptr;").
        self.agregar_estado_final(20, "**")

        # ====================================================
        # DIVISIÓN
        # ====================================================

        self.agregar_transicion(0, "/", 25)
        self.agregar_transicion(25, "=", 60)
        self.agregar_estado_final(25, "/")
        self.agregar_estado_final(60, "/=")

        # ====================================================
        # COMENTARIO DE LÍNEA
        # ====================================================

        self.agregar_transicion(25, "/", 26)
        self.agregar_transicion(26, "CARACTER_LINEA", 27)
        self.agregar_transicion(27, "CARACTER_LINEA", 27)
        self.agregar_estado_final(27, "comLinea")

        # ====================================================
        # COMENTARIO DE BLOQUE
        # ====================================================

        self.agregar_transicion(25, "*", 28)
        # 28: recien abierto "/*". Si el primer caracter del cuerpo ya es
        # '*', debe quedar "en espera de /" (30), no tratarse como cuerpo
        # normal (29); si no, es cuerpo normal.
        self.agregar_transicion(28, "*", 30)
        self.agregar_transicion(28, "CARACTER_COMENTARIO", 29)
        # 29: cuerpo del comentario, sin '*' pendiente.
        self.agregar_transicion(29, "*", 30)
        self.agregar_transicion(29, "CARACTER_COMENTARIO", 29)
        # 30: se vio uno o mas '*' seguidos ("en espera de /").
        # Un '/' cierra el comentario; otro '*' mantiene la espera
        # (soporta "**/", "/**/", "/*** */", etc.); cualquier otro
        # caracter regresa al cuerpo normal.
        self.agregar_transicion(30, "/", 31)
        self.agregar_transicion(30, "*", 30)
        self.agregar_transicion(30, "CARACTER_COMENTARIO", 29)
        self.agregar_estado_final(31, "comBloque")

        # ====================================================
        # IGUAL
        # ====================================================

        self.agregar_transicion(0, "=", 38)
        self.agregar_transicion(38, "=", 39)
        self.agregar_estado_final(38, "=")
        self.agregar_estado_final(39, "==")

        # ====================================================
        # NEGACIÓN
        # ====================================================

        self.agregar_transicion(0, "!", 21)
        self.agregar_transicion(21, "=", 22)
        self.agregar_estado_final(21, "!")
        self.agregar_estado_final(22, "!=")

        # ====================================================
        # MENOR
        # ====================================================

        self.agregar_transicion(0, "<", 47)
        self.agregar_transicion(47, "=", 48)
        self.agregar_transicion(47, "<", 49)
        self.agregar_estado_final(47, "<")
        self.agregar_estado_final(48, "<=")
        self.agregar_estado_final(49, "<<")

        # ====================================================
        # MAYOR
        # ====================================================

        self.agregar_transicion(0, ">", 44)
        self.agregar_transicion(44, "=", 46)
        self.agregar_transicion(44, ">", 45)
        self.agregar_estado_final(44, ">")
        self.agregar_estado_final(46, ">=")
        self.agregar_estado_final(45, ">>")

        # ====================================================
        # &
        # ====================================================

        self.agregar_transicion(0, "&", 42)
        self.agregar_transicion(42, "&", 43)
        self.agregar_estado_final(42, "&")
        self.agregar_estado_final(43, "&&")


        # ====================================================
        # |
        # ====================================================

        self.agregar_transicion(0, "|", 40)
        self.agregar_transicion(40, "|", 41)
        self.agregar_estado_final(40, "|")
        self.agregar_estado_final(41, "||")


        # ====================================================
        # %
        # ====================================================

        self.agregar_transicion(0, "%", 23)
        self.agregar_transicion(23, "=", 24)
        self.agregar_estado_final(23, "%")
        self.agregar_estado_final(24, "%=")

        # ====================================================
        # ?
        # ====================================================

        self.agregar_transicion(0, "?", 37)
        self.agregar_estado_final(37, "?")
        # BARRA INVERSA
        self.agregar_transicion(0,"\\",36)
        self.agregar_estado_final(36,"BARRA_INVERSA")
        # #
        self.agregar_transicion(0,"#",57)
        self.agregar_estado_final(57,"#")
        # ~
        self.agregar_transicion(0,"~",58)
        self.agregar_estado_final(58,"~")
        # ^
        self.agregar_transicion(0,"^",59)
        self.agregar_estado_final(59,"^")

    # ========================================================
    # TRANSITAR
    # ========================================================

    def transitar(
        self,
        estado: int,
        simbolo: str
    ):

        # ----------------------------------------------------
        # PRIMERO: TRANSICIONES LITERALES
        # ----------------------------------------------------

        for transicion in self.transiciones:

            if transicion.estadoOrigen == estado:

                if transicion.simbolo == simbolo:

                    return transicion.estadoDestino

        # ----------------------------------------------------
        # SEGUNDO: TRANSICIONES POR CATEGORÍAS
        # ----------------------------------------------------

        for transicion in self.transiciones:

            if transicion.estadoOrigen == estado:

                if transicion.simbolo != simbolo:

                    if transicion.aplica(simbolo):

                        return transicion.estadoDestino


        return None
    # ========================================================
    # SABER SI ES ESTADO FINAL
    # ========================================================

    def esFinal(
        self,
        estado: int
    ) -> bool:

        return estado in self.estadosFinales
    # ========================================================
    # RECONOCER LEXEMA
    # ========================================================

    def reconocer(
        self,
        lexema: str
    ) -> str:

        estado = self.estadoInicial

        # ----------------------------------------------------
        # RECORRER EL LEXEMA
        # ----------------------------------------------------

        for caracter in lexema:

            nuevo_estado = self.transitar(
                estado,
                caracter
            )

            if nuevo_estado is None:

                return "ERROR"

            estado = nuevo_estado
        # ----------------------------------------------------
        # COMPROBAR ESTADO FINAL
        # ----------------------------------------------------

        if not self.esFinal(estado):

            return "ERROR"

        token = self.estadosFinales[
            estado
        ].aceptacion

        # ----------------------------------------------------
        # IDENTIFICADOR -> PALABRA RESERVADA (con su categoria especifica,
        # ej. "int" -> RESERVADA_TIPO_DATO, "if" -> RESERVADA_CONTROL)
        # ----------------------------------------------------

        if token == "IDENTIFICADOR":

            if lexema in PALABRAS_RESERVADAS:

                return categoria_palabra_reservada(lexema)


        return token
