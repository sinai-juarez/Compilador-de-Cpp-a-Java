%option noyywrap

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ==========================================================
   Analizador Lexico - Lenguaje fuente C++ (compilador C++ -> Java)
   Implementado en Flex de acuerdo con:
     - El AFD (Autómata Finito Determinista) del analizador léxico
       (estados q0..q60, con sus estados finales y el token que
       reconoce cada uno).
     - Las expresiones regulares de la especificación léxica del
       lenguaje (expresiones_regulares.pdf).

   Salidas (mismo formato en consola y en archivo):
     tiraTokens.txt     No linea | lexema | token
     tablaSimbolos.txt  # | Identificador   (en orden de aparicion)
     errores.txt        # | Línea | Columna | Carácter | Descripción

   Nombre del token:
     - palabras reservadas, operadores y delimitadores: el propio
       lexema (int -> int, ( -> (, ** -> **)
     - identificadores: id."valor"      (ej. id."a")
     - numeros: nint.valor / nfloat.valor (ej. nint.1, nfloat.3.14)
     - cadenas y caracteres: literal.valor (ej. literal."hola")

   Errores (mismos mensajes que el analizador de la interfaz):
     - Caracter no reconocido          simbolo fuera del alfabeto
     - Cadena sin cerrar               se descarta el resto del renglon
     - Caracter sin cerrar             se descarta el resto del renglon
     - Comentario de bloque sin cerrar se descarta el resto del archivo
   ========================================================== */

/* Estructura para la Tabla de Simbolos (identificadores) */
typedef struct elemento {
    char nombre[256];
    struct elemento *sig;
} ElementoTSimb;

ElementoTSimb *tSimb = NULL, *temp = NULL, *nuevo = NULL;

/* Punteros para los archivos de salida requeridos */
FILE *tiraTokens = NULL;
FILE *errores = NULL;
FILE *tablaSimbolosArchivo = NULL;

int numLinea   = 1;
int numColumna = 1;   /* columna donde inicia el siguiente lexema a leer */
int colInicio  = 1;   /* columna donde inicio el lexema que se acaba de reconocer */
int numErrores = 0;

/* Actualiza la columna en cada lexema reconocido, antes de ejecutar la
   accion de la regla */
#define YY_USER_ACTION { colInicio = numColumna; numColumna += yyleng; }

/* Declaracion de funciones auxiliares */
void escribirToken(const char *token);
void escribirTokenValor(const char *tipo, const char *comillas);
void escribirError(const char *caracter, const char *mensaje);
void agregarSimbolo(const char nombre[]);
void insertar(ElementoTSimb **tSimb, ElementoTSimb *nuevo);
ElementoTSimb* buscar(ElementoTSimb *tSimb, const char nombre[]);
void imprimirTablaSimbolos(ElementoTSimb *tSimb);
%}

 /* Estados para recuperarse de un error:
    RESTO_LINEA   descarta hasta el fin del renglon (cadena/caracter sin cerrar)
    RESTO_ARCHIVO descarta hasta el fin del archivo (comentario sin cerrar) */
%x RESTO_LINEA RESTO_ARCHIVO

 /* ==========================================================
    1. ALFABETO (expresiones_regulares, seccion 1)
    ========================================================== */
letra             [A-Za-z]
digito            [0-9]

 /* 2. Identificador: letra(letra|digito|_)* */
identificador     {letra}({letra}|{digito}|_)*

 /* 4. Numeros: nint = digito+ ; nfloat = digito+ . digito+
    (coincide con el AFD: q0-D->q32(nint) -.->q33 -D->q34(nfloat)) */
nfloat            {digito}+\.{digito}+
nint              {digito}+

 /* 5. Literales
    escape         = \(" | \ | n | t | r | ' | 0)
    caracterCadena = cualquier caracter excepto comilla doble, diagonal
                     invertida y salto de linea
    cadena         = "(caracterCadena|escape)*"
    caracter       = 'un unico caracter' */
escape            \\(\"|\\|n|t|r|'|0)
caracterCadena    [^"\\\n]
literalCadena     \"({caracterCadena}|{escape})*\"
literalCar        '[^'\n]'

%%

 /* ==========================================================
    1. ESPACIOS Y SALTOS DE LINEA (se descartan / incrementan contador)
    ========================================================== */
[\t\r\v\f ]+      { /* Ignorar espacios, tabuladores, etc. */ }
\n                { numLinea++; numColumna = 1; }

 /* ==========================================================
    2. COMENTARIOS (se descartan) -> q25-/->q26-Cadena->q27(comLinea)
                                      q25-*->q28-Cadena->q29(*)->q30(ComBloque)
    ========================================================== */
"//".*                     { /* Ignorar comentario de linea */ }
"/*"([^*]|\*+[^/*])*\*+"/" {
    int i;
    char *ultimoSalto = strrchr(yytext, '\n');
    for (i = 0; yytext[i] != '\0'; i++) {
        if (yytext[i] == '\n') numLinea++;
    }
    /* si el comentario abarca varias lineas, la columna sigue despues
       del ultimo salto de linea */
    if (ultimoSalto != NULL) numColumna = (int) strlen(ultimoSalto + 1) + 1;
}

 /* ==========================================================
    3. PALABRAS RESERVADAS DE C++ (expresiones_regulares, seccion 3)
       El token es la propia palabra.
    ========================================================== */
"int"|"float"|"double"|"char"|"bool"|"void"|"string"                           { escribirToken(yytext); }
"if"|"else"|"switch"|"case"|"default"|"while"|"do"|"for"|"break"|"continue"|"return" { escribirToken(yytext); }
"true"|"false"                                                                  { escribirToken(yytext); }
"main"                                                                          { escribirToken(yytext); }
"short"|"long"|"signed"|"unsigned"|"const"|"static"                             { escribirToken(yytext); }
"struct"|"class"|"enum"|"public"|"private"|"protected"                          { escribirToken(yytext); }
"new"|"delete"|"sizeof"|"typedef"                                               { escribirToken(yytext); }
"using"|"namespace"                                                             { escribirToken(yytext); }
"cin"|"cout"|"endl"|"std"|"printf"|"scanf"                                      { escribirToken(yytext); }

 /* ==========================================================
    4. OPERADORES (el token es el propio operador)
       Flex siempre toma la coincidencia mas larga, asi que "++" gana
       sobre "+", "<<" sobre "<", etc.
       "**" es el doble apuntador de C++ (ej. int **ptr;), estado
       final q20 del AFD (q18 -*-> q20).
    ========================================================== */
"::"|"**"|"++"|"--"|"+="|"-="|"*="|"/="|"%="|"<="|">="|"=="|"!="|"&&"|"||"|"<<"|">>"|"->" { escribirToken(yytext); }
"+"|"-"|"*"|"/"|"%"|"="|"<"|">"|"!"|"&"|"|"|"^"|"~"|"."|"?"                    { escribirToken(yytext); }

 /* ==========================================================
    5. DELIMITADORES (el token es el propio delimitador)
    ========================================================== */
"{"|"}"|"("|")"|"["|"]"|":"|";"|","|"#"                                        { escribirToken(yytext); }

 /* ==========================================================
    6. NUMEROS, LITERALES E IDENTIFICADORES
    ========================================================== */
{nfloat}          { escribirTokenValor("nfloat", ""); }
{nint}            { escribirTokenValor("nint", ""); }
{literalCadena}   { escribirTokenValor("literal", ""); }
{literalCar}      { escribirTokenValor("literal", ""); }

{identificador}   {
    escribirTokenValor("id", "\"");
    agregarSimbolo(yytext);
}

 /* ==========================================================
    7. ERRORES LEXICOS
       Las reglas de cadena, caracter y comentario completos son mas
       largas, asi que estas solo se aplican cuando NO se cierran.
       Todo lo que sigue en el renglon (o en el archivo) se descarta
       para que no se reporte como tokens ni entre a la tabla de
       simbolos.
    ========================================================== */
\"                { escribirError("\"", "Cadena sin cerrar"); BEGIN(RESTO_LINEA); }
'                 { escribirError("'", "Caracter sin cerrar"); BEGIN(RESTO_LINEA); }
"/*"              { escribirError("/*", "Comentario de bloque sin cerrar"); BEGIN(RESTO_ARCHIVO); }
.                 { escribirError(yytext, "Caracter no reconocido"); }

<RESTO_LINEA>[^\n]+   { /* descartar */ }
<RESTO_LINEA>\n       { numLinea++; numColumna = 1; BEGIN(INITIAL); }
<RESTO_ARCHIVO>(.|\n)+ { /* descartar */ }

%%

/* ==========================================================
                     PROCEDIMIENTOS AUXILIARES
   ========================================================== */

/* Renglon de la tira de tokens: No linea | lexema | token */
void escribirToken(const char *token) {
    printf("%-9d%-26s %s\n", numLinea, yytext, token);
    if (tiraTokens != NULL) {
        fprintf(tiraTokens, "%-9d%-26s %s\n", numLinea, yytext, token);
    }
}

/* Token con valor: tipo.valor (nint.1, literal."hola") o, con comillas,
   tipo."valor" (id."a") */
void escribirTokenValor(const char *tipo, const char *comillas) {
    printf("%-9d%-26s %s.%s%s%s\n", numLinea, yytext, tipo, comillas, yytext, comillas);
    if (tiraTokens != NULL) {
        fprintf(tiraTokens, "%-9d%-26s %s.%s%s%s\n", numLinea, yytext, tipo, comillas, yytext, comillas);
    }
}

/* Renglon de la tabla de errores: # | Linea | Columna | Caracter | Descripcion */
void escribirError(const char *caracter, const char *mensaje) {
    numErrores++;
    fprintf(stderr, "%-5d%-8d%-10d%-11s%s\n", numErrores, numLinea, colInicio, caracter, mensaje);
    if (errores != NULL) {
        fprintf(errores, "%-5d%-8d%-10d%-11s%s\n", numErrores, numLinea, colInicio, caracter, mensaje);
    }
}

/* Inserta el identificador en la Tabla de Simbolos si no existe */
void agregarSimbolo(const char nombre[]) {
    temp = buscar(tSimb, nombre);
    if (temp == NULL) {
        nuevo = (ElementoTSimb*) malloc(sizeof(ElementoTSimb));
        if (nuevo != NULL) {
            strncpy(nuevo->nombre, nombre, sizeof(nuevo->nombre) - 1);
            nuevo->nombre[sizeof(nuevo->nombre) - 1] = '\0';
            insertar(&tSimb, nuevo);
        }
    }
}

/* Inserta al FINAL de la lista, para que la tabla quede en el orden en
   que aparecen los identificadores en el programa */
void insertar(ElementoTSimb **tSimb, ElementoTSimb *nuevo) {
    nuevo->sig = NULL;
    while (*tSimb != NULL) {
        tSimb = &(*tSimb)->sig;
    }
    *tSimb = nuevo;
}

ElementoTSimb* buscar(ElementoTSimb *tSimb, const char nombre[]) {
    while (tSimb != NULL && strcmp(nombre, tSimb->nombre) != 0) {
        tSimb = tSimb->sig;
    }
    return tSimb;
}

/* Tabla de simbolos: # | Identificador */
void imprimirTablaSimbolos(ElementoTSimb *tSimb) {
    int i = 1;
    printf("\nTabla de simbolos\n");
    printf("%-5s%s\n", "#", "Identificador");
    if (tablaSimbolosArchivo != NULL) {
        fprintf(tablaSimbolosArchivo, "%-5s%s\n", "#", "Identificador");
    }
    while (tSimb != NULL) {
        printf("%-5d%s\n", i, tSimb->nombre);
        if (tablaSimbolosArchivo != NULL) {
            fprintf(tablaSimbolosArchivo, "%-5d%s\n", i, tSimb->nombre);
        }
        tSimb = tSimb->sig;
        i++;
    }
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
    } else {
        yyin = fopen("prueba.cpp", "r");
    }

    if (yyin == NULL) {
        perror("Error al abrir el archivo de entrada");
        return 1;
    }

    /* Archivos de salida: tira de tokens, tabla de simbolos y errores */
    tiraTokens = fopen("tiraTokens.txt", "w");
    errores = fopen("errores.txt", "w");
    tablaSimbolosArchivo = fopen("tablaSimbolos.txt", "w");
    tSimb = NULL;

    printf("%-9s%-26s %s\n", "No linea", "lexema", "token");
    if (tiraTokens != NULL) {
        fprintf(tiraTokens, "%-9s%-26s %s\n", "No linea", "lexema", "token");
    }
    /* Encabezado escrito a mano: printf cuenta bytes y las letras con
       acento ocupan 2, asi que %-8s desalinearia las columnas */
    if (errores != NULL) {
        fprintf(errores, "#    Línea   Columna   Carácter   Descripción\n");
    }

    yylex();

    imprimirTablaSimbolos(tSimb);

    if (yyin) fclose(yyin);
    if (tiraTokens) fclose(tiraTokens);
    if (errores) fclose(errores);
    if (tablaSimbolosArchivo) fclose(tablaSimbolosArchivo);

    return 0;
}
