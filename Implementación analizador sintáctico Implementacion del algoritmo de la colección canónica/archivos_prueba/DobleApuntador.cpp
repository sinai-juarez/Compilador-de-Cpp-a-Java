// Ejemplo de doble apuntador (**) en C++
#include <iostream>
using namespace std;

void cambiar(int **ptr, int *nuevo) {
    *ptr = nuevo;
}

int main() {
    int a = 10;
    int b = 20;
    int *p = &a;
    int **pp = &p;

    cout << "Valor de a: " << **pp << endl;

    cambiar(pp, &b);
    cout << "Ahora p apunta a b: " << **pp << endl;

    **pp = 30;
    cout << "b vale: " << b << endl;

    // Matriz dinamica con doble apuntador
    int filas = 2;
    int **matriz = new int*[filas];
    for (int i = 0; i < filas; i++) {
        matriz[i] = new int[3];
    }
    matriz[1][2] = 5;

    delete[] matriz;
    return 0;
}
