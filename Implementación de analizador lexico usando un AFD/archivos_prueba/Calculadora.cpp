using namespace std;

double sumar(double a, double b) {
    return a + b;
}

double dividir(double a, double b) {
    if (b == 0) {
        cout << "No se puede dividir entre cero" << endl;
        return 0;
    }
    return a / b;
}

int main() {
    double x;
    double y;
    int operacion;

    cout << "Primer numero: ";
    cin >> x;
    cout << "Segundo numero: ";
    cin >> y;
    cout << "1) Sumar 2) Dividir: ";
    cin >> operacion;

    if (operacion == 1) {
        cout << "Resultado: " << sumar(x, y) << endl;
    } else if (operacion == 2) {
        cout << "Resultado: " << dividir(x, y) << endl;
    } else {
        cout << "Opcion invalida" << endl;
    }

    return 0;
}
