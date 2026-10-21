// Archivo con errores lexicos a proposito.
// Errores esperados: @ (linea 7), $ (linea 8),
// cadena sin cerrar (linea 9) y caracter sin cerrar (linea 10).
using namespace std;

int main() {
    int a = 5 @ 3;
    int b = $valor;
    string s = "cadena sin cerrar;
    char c = 'x;
    int ok = 10;
    cout << ok << endl;
    return 0;
}
