// Programa de prueba para comentarios
using namespace std;

/* Comentario de bloque
   en varias lineas con simbolos raros: @ $ # ' "
   y un asterisco * suelto y una diagonal / suelta */
int main() {
    int a = 20; // comentario al final de la linea
    int b = 4;  /* comentario de bloque en la misma linea */
    int c = a / b; // una division no es un comentario
    int d = a /* comentario en medio */ + b;

    // // doble comentario de linea
    /* // comentario de linea dentro de un bloque */

    cout << c << endl; // fin
    return 0;
}
